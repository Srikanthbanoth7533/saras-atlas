"""
SARAS ATLAS — Enterprise Data Ingestion Pydantic Schemas.
Defines schemas for CSV/Excel upload preview, schema validation, column mapping,
duplicate detection, missing value imputation, transactional commit, rollback, and data quality.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class IngestionEntity(str, Enum):
    INVENTORY_SNAPSHOT = "INVENTORY_SNAPSHOT"
    PURCHASE_ORDER = "PURCHASE_ORDER"
    SKU_CATALOG = "SKU_CATALOG"
    SALES_ORDER = "SALES_ORDER"


class CanonicalSchemaField(BaseModel):
    """Definition of a canonical ATLAS schema attribute."""
    field_name: str
    data_type: str  # string, integer, float, date, boolean
    required: bool
    description: str
    aliases: List[str] = Field(default_factory=list)


class ValidationIssue(BaseModel):
    """Validation anomaly discovered during pre-flight file parsing."""
    row_index: int
    column: str
    severity: str = "WARNING"  # ERROR, WARNING, INFO
    message: str
    value: Optional[Any] = None


class IngestionPreviewResponse(BaseModel):
    """Pre-flight parsing and validation summary for uploaded dataset."""
    file_id: str
    filename: str
    file_format: str  # CSV or EXCEL
    file_size_bytes: int
    target_entity: IngestionEntity
    total_rows: int
    preview_rows: List[Dict[str, Any]]
    detected_columns: List[str]
    suggested_mapping: Dict[str, str]
    canonical_fields: List[CanonicalSchemaField]
    total_errors: int
    total_warnings: int
    issues_sample: List[ValidationIssue]
    missing_value_summary: Dict[str, int]
    duplicate_rows_count: int
    can_commit: bool


class IngestionCommitRequest(BaseModel):
    """Request to commit a staged file into the transactional warehouse."""
    file_id: str
    target_entity: IngestionEntity
    column_mapping: Dict[str, str]
    deduplication_strategy: str = Field(default="REPLACE_EXISTING", description="REPLACE_EXISTING | SKIP_DUPLICATES | APPEND")
    impute_missing: bool = Field(default=True, description="Auto-impute missing non-critical numerical fields with 0")


class IngestionCommitResponse(BaseModel):
    """Result of committing data into SQLite and Parquet storage."""
    rollback_token: str
    status: str  # COMMITTED, FAILED
    target_entity: IngestionEntity
    rows_processed: int
    rows_inserted: int
    rows_updated: int
    rows_rejected: int
    execution_duration_ms: int
    sha256_checksum: str
    timestamp: str
    lineage_record_id: str
    message: str


class RollbackRequest(BaseModel):
    """Request to undo an ingestion batch."""
    rollback_token: str


class RollbackResponse(BaseModel):
    """Outcome of a transactional rollback operation."""
    rollback_token: str
    status: str  # ROLLED_BACK, NOT_FOUND, FAILED
    restored_entity: str
    message: str
    timestamp: str


class DatasetHealthMetric(BaseModel):
    """Data quality and integrity score for a specific entity."""
    entity_name: str
    total_records: int
    completeness_pct: float
    validity_pct: float
    uniqueness_pct: float
    timeliness_score: float
    health_grade: str  # A+, A, B, C, F


class DataQualityReport(BaseModel):
    """Enterprise-wide data quality health monitor report."""
    overall_health_score: float = Field(..., description="Aggregate health score [0..100]")
    overall_grade: str
    evaluated_records: int
    metrics_by_dataset: List[DatasetHealthMetric]
    system_recommendations: List[str]
    last_audit_timestamp: str

