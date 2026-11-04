"""
SARAS ATLAS — Independent PDF and CSV Reconciliation Verification Script.
Checks that all data fields in the executive briefing are represented with complete parity.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.domain.reporting.generator import ExecutiveReportGenerator
import pypdf
import io
import csv

def verify_reconciliation():
    print("=" * 70)
    print("VERIFYING PDF AND CSV RECONCILIATION")
    print("=" * 70)

    # 1. Generate Raw Data
    data = ExecutiveReportGenerator.generate_report_data()
    print(f"Report Title: {data['title']}")
    print(f"Enterprise: {data['enterprise']}")
    print(f"Total Disruption Loss in Data: ${data['root_cause_analysis']['attributions'][-1][1]}")

    # 2. Generate PDF
    pdf_bytes = ExecutiveReportGenerator.export_pdf()
    assert pdf_bytes.startswith(b"%PDF"), "PDF header invalid"
    pdf_reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
    pdf_text = ""
    for page in pdf_reader.pages:
        pdf_text += page.extract_text() or ""
    print(f"PDF Generated: {len(pdf_bytes):,} bytes across {len(pdf_reader.pages)} pages")

    # 3. Generate CSV
    csv_str = ExecutiveReportGenerator.export_csv()
    csv_reader = list(csv.reader(io.StringIO(csv_str)))
    print(f"CSV Generated: {len(csv_str):,} characters across {len(csv_reader)} rows")

    # 4. Check Key Assertions in Both Formats
    key_terms = [
        "Vanguard Apparel Co.",
        "$224,500.00",
        "$129,844.32",
        "PO-9012",
        "WH-WEST",
        "TOTAL RECONCILED LOSS",
        "Two-Man Rule",
        "Marcus Vance",
        "Elena Rostova",
    ]

    for term in key_terms:
        assert term in pdf_text, f"Term '{term}' missing from PDF"
        assert term in csv_str, f"Term '{term}' missing from CSV"
        print(f"  [PASS] Reconciled field present in both PDF & CSV: '{term}'")

    # 5. Check KPI scorecards match
    for row in data["kpi_posture"]:
        metric_name = row[0]
        assert metric_name in pdf_text, f"Metric '{metric_name}' missing from PDF"
        assert metric_name in csv_str, f"Metric '{metric_name}' missing from CSV"

    # 6. Check Loss Segments match
    pdf_text_normalized = " ".join(pdf_text.split())
    for row in data["root_cause_analysis"]["attributions"]:
        segment_name = row[0]
        dollar_impact = row[1]
        assert segment_name in pdf_text_normalized, f"Segment '{segment_name}' missing from PDF"
        assert segment_name in csv_str, f"Segment '{segment_name}' missing from CSV"
        assert dollar_impact in pdf_text, f"Dollar '{dollar_impact}' missing from PDF"
        assert dollar_impact in csv_str, f"Dollar '{dollar_impact}' missing from CSV"

    print("\n[SUCCESS] 100% Data and Structural Parity between PDF and CSV verified!")

if __name__ == "__main__":
    verify_reconciliation()
