"""
SARAS ATLAS — Root Cause Analysis Routes
"""

from fastapi import APIRouter, Depends, Query
from src.domain.rca.models import RootCauseTraceResponse
from src.domain.rca.tracer import RootCauseTracer
from src.security.models import User
from src.security.auth import get_current_user

router = APIRouter(prefix="/rca", tags=["Root Cause Analysis"])


@router.get("/trace", response_model=RootCauseTraceResponse)
def trace_root_cause(
    disruption_id: str = Query("DISR-PO9012", description="Disruption event identifier"),
    user: User = Depends(get_current_user),
):
    tracer = RootCauseTracer()
    return tracer.trace_disruption(disruption_id=disruption_id)

