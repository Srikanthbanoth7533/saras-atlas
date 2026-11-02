"""
SARAS ATLAS — Unit Tests for Google OR-Tools Prescriptive MILP Solver.
"""

import pytest
from src.database.session import SessionLocal
from src.domain.twin.state import DigitalTwinState
from src.domain.optimization.models import (
    OptimizationRequest,
    ObjectiveType,
    SupplierCandidate,
    TransferCandidate,
)
from src.domain.optimization.solver import PrescriptiveOptimizationSolver


@pytest.fixture
def twin_state():
    with SessionLocal() as session:
        twin = DigitalTwinState(session=session)
        yield twin


def test_milp_solver_convergence_and_speed(twin_state):
    """Verify OR-Tools SCIP solver converges to optimality in under 1 second."""
    solver = PrescriptiveOptimizationSolver(twin_state=twin_state)
    req = OptimizationRequest(
        capital_budget_ceiling=40000.00,
        min_service_fill_rate=0.95,
        max_ad_throttle_pct=0.35,
        target_sku="APEX-JKT"
    )

    result = solver.solve(req)

    assert result.status == "OPTIMAL"
    assert result.solve_time_ms < 1000
    assert result.capital_required <= 40000.00
    assert result.recommended_air_freight_units >= 500  # Enforces MOQ
    assert result.projected_stockout_days == 0
    assert result.projected_fill_rate >= 0.95
    assert result.projected_net_contribution_margin > 400000.00


def test_milp_budget_ceiling_enforcement(twin_state):
    """Verify solver strictly respects constrained capital budget ceiling."""
    solver = PrescriptiveOptimizationSolver(twin_state=twin_state)
    # Tight budget: $12,000 max outlay
    req = OptimizationRequest(
        capital_budget_ceiling=12000.00,
        min_service_fill_rate=0.85,
        max_ad_throttle_pct=0.35,
        target_sku="APEX-JKT"
    )

    result = solver.solve(req)

    assert result.status in ("OPTIMAL", "FEASIBLE")
    assert result.capital_required <= 12000.00
    # Because budget is constrained, ad throttle is actively utilized
    assert result.recommended_ad_throttle_pct > 0.10


def test_milp_minimize_working_capital_objective(twin_state):
    """Verify MINIMIZE_WORKING_CAPITAL objective deploys minimum necessary cash."""
    solver = PrescriptiveOptimizationSolver(twin_state=twin_state)
    req = OptimizationRequest(
        capital_budget_ceiling=40000.00,
        min_service_fill_rate=0.90,
        max_ad_throttle_pct=0.35,
        objective=ObjectiveType.MINIMIZE_WORKING_CAPITAL
    )

    result = solver.solve(req)

    assert result.status == "OPTIMAL"
    # Prioritizes cheaper inter-warehouse transfers ($3.20/unit) and max ad throttle over air freight
    assert result.recommended_transfer_units == 800  # Max transfer capacity utilized
    assert result.capital_required < 25000.00

