"""
SARAS ATLAS — Executive Reporting Routes
"""

from fastapi import APIRouter, Depends, Response
from fastapi.responses import StreamingResponse
import io
from src.domain.reporting.generator import ExecutiveReportGenerator
from src.security.models import User
from src.security.auth import get_current_user

router = APIRouter(prefix="/reports", tags=["Executive Reporting"])


@router.get("/summary")
def get_report_summary(user: User = Depends(get_current_user)):
    return ExecutiveReportGenerator.generate_report_data()


@router.get("/export/pdf")
def export_pdf_report(user: User = Depends(get_current_user)):
    pdf_bytes = ExecutiveReportGenerator.export_pdf()
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": 'attachment; filename="saras_atlas_executive_resilience_report.pdf"'
        },
    )


@router.get("/export/csv")
def export_csv_report(user: User = Depends(get_current_user)):
    csv_text = ExecutiveReportGenerator.export_csv()
    return Response(
        content=csv_text,
        media_type="text/csv",
        headers={
            "Content-Disposition": 'attachment; filename="saras_atlas_executive_resilience_report.csv"'
        },
    )

