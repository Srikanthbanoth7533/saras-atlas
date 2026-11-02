"""
SARAS ATLAS — Data Ingestion Parser & Pre-Flight Validator.
Parses CSV and Excel files, generates schema mappings, detects duplicates,
flags missing values, and produces interactive preview responses.
"""

import io
import os
import json
import uuid
import hashlib
from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np

from src.domain.ingestion.models import (
    IngestionEntity,
    IngestionPreviewResponse,
    ValidationIssue,
)
from src.domain.ingestion.schemas import CANONICAL_SCHEMAS, suggest_column_mapping


STAGING_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "data", "staging")
os.makedirs(STAGING_DIR, exist_ok=True)


class IngestionValidator:
    """Pre-flight validator for enterprise datasets prior to transactional commit."""

    @staticmethod
    def parse_file_to_dataframe(file_bytes: bytes, filename: str) -> Tuple[pd.DataFrame, str]:
        """Parses CSV or Excel file bytes into a Pandas DataFrame."""
        ext = os.path.splitext(filename)[1].lower()
        if ext in [".xlsx", ".xls"]:
            df = pd.read_excel(io.BytesIO(file_bytes), engine="openpyxl")
            fmt = "EXCEL"
        else:
            # Attempt UTF-8, then fallback to Latin-1
            try:
                df = pd.read_csv(io.BytesIO(file_bytes), encoding="utf-8")
            except UnicodeDecodeError:
                df = pd.read_csv(io.BytesIO(file_bytes), encoding="latin-1")
            fmt = "CSV"
        return df, fmt

    @classmethod
    def generate_preview(
        cls,
        file_bytes: bytes,
        filename: str,
        target_entity: IngestionEntity,
    ) -> IngestionPreviewResponse:
        """Parses file and returns a pre-flight preview and validation assessment."""
        file_size = len(file_bytes)
        sha256_hash = hashlib.sha256(file_bytes).hexdigest()
        file_id = f"FILE-{uuid.uuid4().hex[:8].upper()}"

        df, file_format = cls.parse_file_to_dataframe(file_bytes, filename)
        total_rows = len(df)
        detected_cols = [str(c) for c in df.columns]

        # 1. Column mapping suggestion
        suggested_mapping = suggest_column_mapping(detected_cols, target_entity)
        canonical_fields = CANONICAL_SCHEMAS.get(target_entity, [])

        # 2. Check for missing values
        missing_summary: Dict[str, int] = {}
        for col in df.columns:
            null_count = int(df[col].isna().sum())
            if null_count > 0:
                missing_summary[str(col)] = null_count

        # 3. Check for duplicates
        duplicate_count = int(df.duplicated().sum())

        # 4. Pre-flight schema validation checks
        issues: List[ValidationIssue] = []
        errors_count = 0
        warnings_count = 0

        # Check required canonical fields
        mapped_canonicals = set(suggested_mapping.values())
        for req_field in canonical_fields:
            if req_field.required and req_field.field_name not in mapped_canonicals:
                issues.append(
                    ValidationIssue(
                        row_index=0,
                        column="<MAPPING>",
                        severity="ERROR",
                        message=f"Required canonical field '{req_field.field_name}' ({req_field.description}) is not mapped.",
                        value=None,
                    )
                )
                errors_count += 1

        # Inspect first 100 rows for data type anomalies
        sample_check_limit = min(100, total_rows)
        for col, canon_name in suggested_mapping.items():
            field_meta = next((f for f in canonical_fields if f.field_name == canon_name), None)
            if not field_meta:
                continue

            for idx in range(sample_check_limit):
                val = df[col].iloc[idx]
                if pd.isna(val):
                    if field_meta.required:
                        if len(issues) < 20:
                            issues.append(
                                ValidationIssue(
                                    row_index=idx + 1,
                                    column=str(col),
                                    severity="WARNING",
                                    message=f"Missing required value for '{canon_name}'.",
                                    value="NULL",
                                )
                            )
                        warnings_count += 1
                    continue

                # Type checks
                if field_meta.data_type == "integer":
                    try:
                        int_val = int(val)
                        if int_val < 0 and "cost" not in canon_name and "margin" not in canon_name:
                            if len(issues) < 20:
                                issues.append(
                                    ValidationIssue(
                                        row_index=idx + 1,
                                        column=str(col),
                                        severity="WARNING",
                                        message=f"Negative value ({int_val}) found in count field '{canon_name}'.",
                                        value=int_val,
                                    )
                                )
                            warnings_count += 1
                    except (ValueError, TypeError):
                        if len(issues) < 20:
                            issues.append(
                                ValidationIssue(
                                    row_index=idx + 1,
                                    column=str(col),
                                    severity="ERROR",
                                    message=f"Expected integer for '{canon_name}', got '{val}'.",
                                    value=str(val),
                                )
                            )
                        errors_count += 1

                elif field_meta.data_type == "float":
                    try:
                        float_val = float(val)
                        if float_val < 0 and "margin" not in canon_name and "delta" not in canon_name:
                            if len(issues) < 20:
                                issues.append(
                                    ValidationIssue(
                                        row_index=idx + 1,
                                        column=str(col),
                                        severity="WARNING",
                                        message=f"Negative numerical value ({float_val}) in '{canon_name}'.",
                                        value=float_val,
                                    )
                                )
                            warnings_count += 1
                    except (ValueError, TypeError):
                        if len(issues) < 20:
                            issues.append(
                                ValidationIssue(
                                    row_index=idx + 1,
                                    column=str(col),
                                    severity="ERROR",
                                    message=f"Expected float number for '{canon_name}', got '{val}'.",
                                    value=str(val),
                                )
                            )
                        errors_count += 1

        # 5. Extract top preview rows (up to 5 rows formatted for JSON)
        preview_df = df.head(5).copy()
        # Convert NaNs to None for clean JSON serialization
        preview_rows = json.loads(preview_df.to_json(orient="records", date_format="iso"))

        # 6. Save staged data locally for subsequent commit
        stage_meta = {
            "file_id": file_id,
            "filename": filename,
            "file_format": file_format,
            "sha256": sha256_hash,
            "total_rows": total_rows,
            "target_entity": target_entity.value,
            "detected_columns": detected_cols,
            "suggested_mapping": suggested_mapping,
        }
        meta_path = os.path.join(STAGING_DIR, f"{file_id}.json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(stage_meta, f, indent=2)

        data_path = os.path.join(STAGING_DIR, f"{file_id}.csv")
        df.to_csv(data_path, index=False)

        can_commit = (errors_count == 0)

        return IngestionPreviewResponse(
            file_id=file_id,
            filename=filename,
            file_format=file_format,
            file_size_bytes=file_size,
            target_entity=target_entity,
            total_rows=total_rows,
            preview_rows=preview_rows,
            detected_columns=detected_cols,
            suggested_mapping=suggested_mapping,
            canonical_fields=canonical_fields,
            total_errors=errors_count,
            total_warnings=warnings_count,
            issues_sample=issues[:15],
            missing_value_summary=missing_summary,
            duplicate_rows_count=duplicate_count,
            can_commit=can_commit,
        )
