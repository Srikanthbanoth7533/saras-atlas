"""
SARAS ATLAS — Sentinel Risk Detection Router.
Monitors the digital twin for supply delays, freight surcharges, and stockout horizons.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.session import SessionLocal
from src.domain.twin.state import DigitalTwinState
from src.domain.twin.sentinels import OperationalRiskSentinel

router = APIRouter(prefix="/risks", tags=["Risk Sentinels"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/active")
def get_active_risks(session: Session = Depends(get_db)):
    """Runs automated operational risk sentinels and returns prioritized alerts."""
    twin = DigitalTwinState(session=session)
    sentinel = OperationalRiskSentinel(twin)
    risks = sentinel.detect_active_risks()
    return {
        "status": "SCANNED",
        "total_active_risks": len(risks),
        "critical_count": sum(1 for r in risks if r["severity"] == "CRITICAL"),
        "warning_count": sum(1 for r in risks if r["severity"] == "WARNING"),
        "risks": risks,
    }
