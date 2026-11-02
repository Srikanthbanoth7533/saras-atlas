"""
SARAS ATLAS — Scenario Simulation & Comparison Router.
Executes multi-echelon discrete difference simulations and comparative analysis.
"""

from typing import List
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.session import SessionLocal
from src.database.models.simulation import Scenario, SimulationRun
from src.domain.twin.state import DigitalTwinState
from src.domain.simulation.engine import SimulationEngine
from src.domain.simulation.models import (
    SimulationRequest,
    SimulationResponse,
)

router = APIRouter(prefix="/scenarios", tags=["Scenario Simulation"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ScenarioComparisonRequest(BaseModel):
    baseline_request: SimulationRequest
    mitigated_request: SimulationRequest


class ScenarioComparisonResponse(BaseModel):
    baseline_result: SimulationResponse
    mitigated_result: SimulationResponse
    net_margin_delta: float = Field(..., description="Protected Net CM ($)")
    revenue_saved: float = Field(..., description="Revenue saved ($)")
    stockout_days_saved: int = Field(..., description="Days of stockout avoided")
    executive_verdict: str = Field(..., description="Prescriptive synthesis")


@router.post("/simulate", response_model=SimulationResponse)
def simulate_scenario(request: SimulationRequest, session: Session = Depends(get_db)):
    """Executes a 90-day multi-echelon scenario simulation and records the run."""
    twin = DigitalTwinState(session=session)
    engine = SimulationEngine(twin)
    response = engine.run_simulation(request)

    # Find or create Scenario entity for foreign key relationship
    scenario = (
        session.query(Scenario)
        .filter(Scenario.org_id == twin.org_id, Scenario.name == request.scenario_name)
        .first()
    )
    if not scenario:
        is_mit = (
            request.mitigations.emergency_air_freight_units > 0
            or request.mitigations.inter_warehouse_transfer_units > 0
            or request.mitigations.ad_spend_throttle_percentage > 0
        )
        scenario = Scenario(
            org_id=twin.org_id,
            name=request.scenario_name,
            scenario_type="MITIGATION_OPTIMAL" if is_mit else "DISRUPTION",
            description="Dynamic simulation run from API request",
            is_active=True,
        )
        session.add(scenario)
        session.flush()

    # Persist simulation run record for audit trail
    run_record = SimulationRun(
        scenario_id=scenario.id,
        execution_duration_ms=response.execution_duration_ms,
        horizon_days=request.horizon_days,
        total_projected_revenue=response.summary_scorecard.net_revenue,
        total_projected_cogs=response.summary_scorecard.cogs_total,
        total_projected_freight=response.summary_scorecard.freight_total,
        total_projected_contribution_margin=response.summary_scorecard.net_contribution_margin,
        projected_margin_rate=response.summary_scorecard.contribution_margin_pct,
        total_lost_revenue_stockouts=response.summary_scorecard.unfulfilled_lost_orders * 180.00,
        stockout_days_count=response.summary_scorecard.stockout_days,
        working_capital_required=response.summary_scorecard.working_capital_required,
        timeseries_payload=response.daily_timeseries,
    )
    session.add(run_record)
    session.commit()

    return response


@router.post("/compare", response_model=ScenarioComparisonResponse)
def compare_scenarios(comparison_req: ScenarioComparisonRequest, session: Session = Depends(get_db)):
    """Runs baseline and mitigated scenarios side-by-side and outputs variance analysis."""
    twin = DigitalTwinState(session=session)
    engine = SimulationEngine(twin)

    base_resp = engine.run_simulation(comparison_req.baseline_request)
    mit_resp = engine.run_simulation(comparison_req.mitigated_request)

    margin_delta = round(
        mit_resp.summary_scorecard.net_contribution_margin - base_resp.summary_scorecard.net_contribution_margin, 2
    )
    rev_saved = round(
        mit_resp.summary_scorecard.net_revenue - base_resp.summary_scorecard.net_revenue, 2
    )
    days_saved = max(
        0, base_resp.summary_scorecard.stockout_days - mit_resp.summary_scorecard.stockout_days
    )

    verdict = (
        f"Implementing '{comparison_req.mitigated_request.scenario_name}' avoids {days_saved} stockout days, "
        f"protects ${rev_saved:,.2f} in gross revenue, and preserves ${margin_delta:,.2f} in net contribution margin "
        f"(ending margin {mit_resp.summary_scorecard.contribution_margin_pct * 100:.1f}% vs "
        f"{base_resp.summary_scorecard.contribution_margin_pct * 100:.1f}% unmitigated)."
    )

    return ScenarioComparisonResponse(
        baseline_result=base_resp,
        mitigated_result=mit_resp,
        net_margin_delta=margin_delta,
        revenue_saved=rev_saved,
        stockout_days_saved=days_saved,
        executive_verdict=verdict,
    )
