"""
SARAS ATLAS — Phase 3 Unit Tests.
Tests Batch Simulation Engine, Dynamic Policy Optimization, Sourcing Optimizer,
Enterprise Data Ingestion, Transactional Rollback, and Data Quality Audits.
"""

import pytest
from src.database.session import SessionLocal
from src.domain.twin.state import DigitalTwinState
from src.domain.batch.engine import BatchSimulationEngine
from src.domain.batch.models import BatchRunRequest, SensitivitySweepRequest
from src.domain.policy.evaluator import PolicyEvaluator
from src.domain.policy.models import PolicyOptimizationRequest, SupplierSourcingRequest
from src.domain.ingestion.validator import IngestionValidator
from src.domain.ingestion.pipeline import IngestionPipeline
from src.domain.ingestion.models import IngestionEntity, IngestionCommitRequest, RollbackRequest


@pytest.fixture(scope="module")
def db_session():
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="module")
def twin_state(db_session):
    return DigitalTwinState(session=db_session)


def test_batch_simulation_execution_and_ranking(twin_state, db_session):
    """Verifies batch execution of 10 scenarios, multi-criteria ranking, and statistics."""
    engine = BatchSimulationEngine(twin_state=twin_state, session=db_session)
    scenarios = engine.generate_benchmark_scenarios(count=10, seed=42)
    assert len(scenarios) == 10

    req = BatchRunRequest(
        batch_name="Test Batch 10",
        scenarios=scenarios,
        parallel=True,
        max_workers=2,
        persist_results=True,
        random_seed=42,
    )
    resp = engine.run_batch(req)

    assert resp.completed_scenarios == 10
    assert resp.failed_scenarios == 0
    assert resp.total_execution_ms > 0
    assert resp.mean_execution_ms_per_scenario < 20.0  # Under 20 ms per scenario
    assert resp.best_case is not None
    assert resp.worst_case is not None
    assert resp.baseline is not None
    assert resp.best_case.composite_score >= resp.worst_case.composite_score
    assert len(resp.ranked_results) == 10
    assert resp.ranked_results[0].rank == 1


def test_parametric_sensitivity_sweep(twin_state, db_session):
    """Verifies 1D sensitivity parameter sweep across supplier delays."""
    engine = BatchSimulationEngine(twin_state=twin_state, session=db_session)
    req = SensitivitySweepRequest(
        parameter="supplier_delay",
        min_value=0,
        max_value=60,
        steps=5,
    )
    resp = engine.run_sensitivity_sweep(req)

    assert resp.steps_evaluated == 5
    assert len(resp.points) == 5
    # As delay increases, stockout days should increase or stay same
    assert resp.points[-1].stockout_days >= resp.points[0].stockout_days
    assert len(resp.executive_insight) > 20


def test_dynamic_policy_evaluation_and_pareto(twin_state, db_session):
    """Verifies stochastic policy evaluation, CVaR risk calculations, and Pareto frontier."""
    evaluator = PolicyEvaluator(twin_state=twin_state, session=db_session)
    req = PolicyOptimizationRequest(num_stochastic_draws=15, random_seed=42)
    resp = evaluator.evaluate_policies(req)

    assert len(resp.evaluated_policies) >= 6
    assert resp.stochastic_draws == 15
    assert resp.recommended_policy_id is not None
    assert len(resp.pareto_frontier) >= 4

    # Verify at least one policy is on the Pareto frontier
    pareto_optimal_count = sum(1 for p in resp.pareto_frontier if p.is_pareto_optimal)
    assert pareto_optimal_count >= 1

    # Check top-ranked policy
    top_policy = resp.evaluated_policies[0]
    assert top_policy.rank == 1
    assert top_policy.mean_cm > 0
    assert top_policy.cvar_90 <= top_policy.mean_cm  # CVaR is downside risk


def test_supplier_dual_sourcing_optimization(twin_state, db_session):
    """Verifies mathematical optimization of dual-sourcing allocation (Shenzhen vs Saigon)."""
    evaluator = PolicyEvaluator(twin_state=twin_state, session=db_session)
    req = SupplierSourcingRequest(
        annual_demand_units=150000,
        shenzhen_unit_cogs=45.15,
        shenzhen_disruption_probability=0.25,
        saigon_unit_cogs=49.50,
        saigon_disruption_probability=0.08,
    )
    resp = evaluator.optimize_supplier_sourcing(req)

    assert 0.0 < resp.optimal_shenzhen_share < 1.0
    assert 0.0 < resp.optimal_saigon_share < 1.0
    assert round(resp.optimal_shenzhen_share + resp.optimal_saigon_share, 2) == 1.00
    assert resp.net_portfolio_savings > 0
    assert resp.optimal_service_level > 0.90


def test_enterprise_data_ingestion_and_rollback():
    """Verifies CSV parsing, preview, schema mapping, transactional commit, and safe rollback."""
    csv_bytes = (
        b"sku_id,warehouse_code,quantity_on_hand,safety_stock_buffer\n"
        b"APEX-JKT-BLA-XS,reno,750,250\n"
        b"APEX-JKT-BLA-S,allentown,920,300\n"
    )

    # 1. Preview
    prev = IngestionValidator.generate_preview(
        file_bytes=csv_bytes,
        filename="batch_inventory_test.csv",
        target_entity=IngestionEntity.INVENTORY_SNAPSHOT,
    )
    assert prev.total_rows == 2
    assert prev.can_commit is True
    assert "sku_id" in prev.suggested_mapping
    assert prev.suggested_mapping["sku_id"] == "sku_code"

    # 2. Commit
    commit_req = IngestionCommitRequest(
        file_id=prev.file_id,
        target_entity=prev.target_entity,
        column_mapping=prev.suggested_mapping,
        deduplication_strategy="REPLACE_EXISTING",
    )
    commit_resp = IngestionPipeline.commit_dataset(commit_req)
    assert commit_resp.status == "COMMITTED"
    assert commit_resp.rollback_token.startswith("RB-")

    # 3. Rollback
    rb_req = RollbackRequest(rollback_token=commit_resp.rollback_token)
    rb_resp = IngestionPipeline.rollback_dataset(rb_req)
    assert rb_resp.status == "ROLLED_BACK"

    # 4. Data Quality Audit
    dq_report = IngestionPipeline.audit_data_quality()
    assert dq_report.overall_health_score > 90.0
    assert dq_report.overall_grade in ["A+", "A"]
    assert len(dq_report.metrics_by_dataset) == 4

