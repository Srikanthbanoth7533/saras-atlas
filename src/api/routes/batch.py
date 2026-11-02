"""
SARAS ATLAS — Multi-Scenario Batch Simulation Router.
Exposes endpoints for parallel batch execution, sensitivity sweeps, benchmark runs, and history.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from src.database.session import SessionLocal
from src.database.models.simulation import Scenario, SimulationRun
from src.domain.twin.state import DigitalTwinState
from src.domain.batch.models import (
    BatchRunRequest,
    BatchRunResponse,
    SensitivitySweepRequest,
    SensitivitySweepResponse,
    BatchScenarioItem,
)
from src.domain.batch.engine import BatchSimulationEngine


router = APIRouter(prefix="/batch", tags=["Batch Scenario Engine"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/run", response_model=BatchRunResponse)
def run_batch_scenarios(
    request: BatchRunRequest,
    session: Session = Depends(get_db),
):
    """Executes a batch of scenarios with multi-threading, ranking, and persistence."""
    try:
        twin = DigitalTwinState(session=session)
        engine = BatchSimulationEngine(twin_state=twin, session=session)
        return engine.run_batch(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch execution failed: {str(e)}")


@router.get("/generate-benchmark", response_model=List[BatchScenarioItem])
def generate_benchmark_scenarios(
    count: int = Query(default=10, ge=3, le=100, description="Number of scenarios to generate"),
    seed: int = Query(default=42, description="Random seed"),
):
    """Generates deterministic benchmark scenarios exploring delays, surcharges, and surges."""
    return BatchSimulationEngine.generate_benchmark_scenarios(count=count, seed=seed)


@router.post("/sensitivity", response_model=SensitivitySweepResponse)
def run_sensitivity_analysis(
    request: SensitivitySweepRequest,
    session: Session = Depends(get_db),
):
    """Executes a 1D parametric sensitivity sweep across delay, surcharge, or demand surge."""
    try:
        twin = DigitalTwinState(session=session)
        engine = BatchSimulationEngine(twin_state=twin, session=session)
        return engine.run_sensitivity_sweep(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sensitivity sweep failed: {str(e)}")


@router.get("/history")
def get_batch_run_history(
    limit: int = Query(default=10, ge=1, le=50),
    session: Session = Depends(get_db),
):
    """Retrieves recent persisted batch runs and execution timestamps."""
    scenarios = (
        session.query(Scenario)
        .filter(Scenario.scenario_type == "BATCH_RUN")
        .order_by(Scenario.created_at.desc())
        .limit(limit)
        .all()
    )
    history = []
    for s in scenarios:
        run_count = session.query(SimulationRun).filter(SimulationRun.scenario_id == s.id).count()
        history.append({
            "batch_id": s.id,
            "batch_name": s.name,
            "created_at": s.created_at.isoformat() if s.created_at else None,
            "scenario_count": run_count,
        })
    return history

