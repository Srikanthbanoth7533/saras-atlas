"""
SARAS ATLAS — Dynamic Policy Optimization & Multi-Sourcing Router.
Exposes endpoints for stochastic policy evaluation, Pareto trade-off curves,
and risk-hedged dual-sourcing allocation.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.session import SessionLocal
from src.domain.twin.state import DigitalTwinState
from src.domain.policy.models import (
    PolicyDefinition,
    PolicyOptimizationRequest,
    PolicyOptimizationResponse,
    SupplierSourcingRequest,
    SupplierSourcingResponse,
)
from src.domain.policy.evaluator import PolicyEvaluator


router = APIRouter(prefix="/policy", tags=["Dynamic Policy Optimization"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/standard-suite", response_model=List[PolicyDefinition])
def get_standard_policy_suite():
    """Returns the baseline candidate mitigation policies."""
    return PolicyEvaluator.get_standard_policy_suite()


@router.post("/evaluate", response_model=PolicyOptimizationResponse)
def evaluate_mitigation_policies(
    request: PolicyOptimizationRequest,
    session: Session = Depends(get_db),
):
    """Evaluates candidate policies across stochastic shock distributions."""
    try:
        twin = DigitalTwinState(session=session)
        evaluator = PolicyEvaluator(twin_state=twin, session=session)
        return evaluator.evaluate_policies(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Policy evaluation failed: {str(e)}")


@router.post("/sourcing", response_model=SupplierSourcingResponse)
def optimize_supplier_sourcing(
    request: SupplierSourcingRequest,
    session: Session = Depends(get_db),
):
    """Solves the risk-hedged procurement allocation between Primary and Backup suppliers."""
    try:
        twin = DigitalTwinState(session=session)
        evaluator = PolicyEvaluator(twin_state=twin, session=session)
        return evaluator.optimize_supplier_sourcing(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sourcing optimization failed: {str(e)}")

