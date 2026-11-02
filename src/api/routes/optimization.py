"""
SARAS ATLAS — Prescriptive Optimization Router.
Executes Google OR-Tools MILP solver for multi-echelon inventory and financial optimization.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.session import SessionLocal
from src.domain.twin.state import DigitalTwinState
from src.domain.optimization.models import (
    OptimizationRequest,
    OptimizationResult,
)
from src.domain.optimization.solver import PrescriptiveOptimizationSolver

router = APIRouter(prefix="/optimization", tags=["Prescriptive Optimization"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/solve", response_model=OptimizationResult)
def solve_optimization(request: OptimizationRequest, session: Session = Depends(get_db)):
    """Solves the multi-echelon MILP decision model using Google OR-Tools SCIP."""
    twin = DigitalTwinState(session=session)
    solver = PrescriptiveOptimizationSolver(twin_state=twin)
    return solver.solve(request)

