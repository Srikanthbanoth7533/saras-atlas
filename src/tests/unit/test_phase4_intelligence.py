"""
SARAS ATLAS — Phase 4 Unit Test Suite
Validates AI Decision Intelligence, Root Cause Analysis, Explainability Dossiers,
Advanced Forecasting against held-out data, Enterprise Connectors, Reporting, and RBAC Security.
"""

import pytest
from src.security.auth import authenticate_user, create_access_token, hash_password, DEMO_USERS
from src.security.models import UserRole, User
from src.security.audit import log_security_event, read_audit_logs
from src.domain.intelligence.engine import DecisionIntelligenceEngine
from src.domain.intelligence.models import QuestionRequest, QueryTopic
from src.domain.rca.tracer import RootCauseTracer
from src.domain.explainability.recommendations import ExplainableRecommendationBuilder
from src.domain.forecasting.engine import AdvancedForecaster
from src.domain.forecasting.models import ForecastSeriesType
from src.domain.connectors.manager import EnterpriseConnectorManager
from src.domain.connectors.models import ConnectorType
from src.domain.reporting.generator import ExecutiveReportGenerator


def test_security_rbac_and_jwt():
    # 1. Successful authentication
    admin = authenticate_user("admin", "AtlasAdmin2026!")
    assert admin is not None
    assert admin.role == UserRole.ADMIN

    # 2. Rejection of bad password
    bad = authenticate_user("admin", "WrongPassword123")
    assert bad is None

    # 3. Token generation & claims
    token = create_access_token(admin)
    assert isinstance(token, str) and len(token) > 20

    # 4. Role identification
    vp = authenticate_user("vp_supply", "SupplyChain2026!")
    assert vp.role == UserRole.SUPPLY_CHAIN_VP


def test_security_audit_logger():
    entry = log_security_event(
        user_id="USR-TEST-01",
        username="test_auditor",
        role="AUDITOR",
        action="TEST_VERIFICATION",
        resource="test_resource",
        status="SUCCESS",
        details={"test_key": "test_val"},
    )
    assert entry.event_id.startswith("EVT-")

    logs = read_audit_logs(limit=10)
    assert len(logs) > 0
    assert any(log.action == "TEST_VERIFICATION" for log in logs)


def test_decision_intelligence_grounding():
    engine = DecisionIntelligenceEngine()

    # Query 1: Inventory intent
    res1 = engine.answer_question(QuestionRequest(query="What is our current stockout risk and days of coverage?"))
    assert res1.intent_topic in [QueryTopic.INVENTORY, QueryTopic.WAREHOUSES]
    assert res1.confidence_score >= 0.70
    assert len(res1.citations) > 0
    assert "WH-WEST" in res1.answer_markdown
    assert res1.data_freshness == "VERIFIED_LIVE_TWIN_DATA"

    # Query 2: Margin / Exposure intent
    res2 = engine.answer_question(QuestionRequest(query="How does the disruption impact our GAAP contribution margin?"))
    assert res2.intent_topic in [QueryTopic.MARGINS, QueryTopic.EXPOSURE]
    assert len(res2.citations) > 0
    assert "$71.33" in res2.answer_markdown
    assert "$58.33" in res2.answer_markdown


def test_root_cause_analysis_tracer():
    tracer = RootCauseTracer()
    rca = tracer.trace_disruption("DISR-PO9012")

    assert "PO-9012" in rca.primary_root_cause
    assert len(rca.causal_chain) >= 5
    assert rca.total_financial_impact == 224500.00

    # Verify financial attribution sums to ~100%
    pct_sum = sum(seg.percentage_of_total for seg in rca.financial_attribution)
    assert 99.0 <= pct_sum <= 101.0

    # Verify top influential variables
    assert len(rca.top_influential_variables) >= 5
    assert rca.top_influential_variables[0].elasticity_rank == 1


def test_explainable_recommendation_builder():
    dossier = ExplainableRecommendationBuilder.build_standard_dossier()

    assert dossier.solver_status == "OPTIMAL"
    assert len(dossier.recommendations) >= 4
    assert dossier.total_expected_financial_benefit > dossier.total_required_capital
    assert dossier.net_roi_multiple > 1.0

    # Test all 8 required explainability fields on every recommendation
    for rec in dossier.recommendations:
        assert len(rec.what_action) > 10
        assert len(rec.why_recommended) > 10
        assert len(rec.expected_financial_benefits) > 5
        assert len(rec.required_capital) > 5
        assert len(rec.operational_tradeoffs) > 10
        assert len(rec.risks_and_assumptions) > 10
        assert len(rec.alternative_actions) >= 2
        assert len(rec.consequences_of_no_action) > 10


def test_advanced_forecaster_heldout_evaluation():
    forecaster = AdvancedForecaster(seed=42)
    res = forecaster.evaluate_forecast(
        series_type=ForecastSeriesType.DAILY_DEMAND,
        train_split_ratio=0.78,
        horizon_days=30,
    )

    # 1. Verify train/test split partitioning
    assert res.train_periods + res.test_periods == 90
    assert res.forecast_horizon == 30

    # 2. Verify all 3 models evaluated on held-out test data
    assert len(res.models_evaluated) == 3
    for model in res.models_evaluated:
        assert model.mae > 0.0
        assert model.rmse > 0.0
        assert 0.0 < model.wape < 50.0  # WAPE within reasonable bounds

    # 3. Verify best model selection
    assert any(m.is_best_model for m in res.models_evaluated)

    # 4. Verify trajectory has prediction intervals
    horizon_points = [p for p in res.forecast_trajectory if p.is_forecast_horizon]
    assert len(horizon_points) == 30
    for p in horizon_points:
        assert p.lower_95 <= p.lower_80 <= p.predicted <= p.upper_80 <= p.upper_95


def test_enterprise_connectors_manager():
    # 1. Connector catalog listing
    connectors = EnterpriseConnectorManager.list_connectors()
    assert len(connectors) >= 5
    types = [c.connector_type for c in connectors]
    assert ConnectorType.BIGQUERY in types
    assert ConnectorType.SNOWFLAKE in types
    assert ConnectorType.AMAZON_REDSHIFT in types

    # 2. Zero-cost sandbox connectivity test
    test_res = EnterpriseConnectorManager.test_connection("CONN-BQ-01")
    assert test_res.success is True
    assert test_res.discovered_tables_count >= 3
    assert test_res.security_posture == "ZERO_CREDENTIAL_LEAK_CONFIRMED"

    # 3. Schema discovery
    schema_res = EnterpriseConnectorManager.discover_schema("CONN-SNOW-02")
    assert "orders_fact" in schema_res.tables
    assert schema_res.dialect == "Snowflake ANSI SQL"


def test_executive_report_pdf_and_csv_generation():
    # 1. PDF generation
    pdf_bytes = ExecutiveReportGenerator.export_pdf()
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 2000
    assert pdf_bytes.startswith(b"%PDF")

    # 2. CSV generation
    csv_text = ExecutiveReportGenerator.export_csv()
    assert isinstance(csv_text, str)
    assert "SARAS ATLAS" in csv_text
    assert "SECTION 1: STRATEGIC KPI SCORECARD" in csv_text
    assert "SECTION 2: ROOT CAUSE ANALYSIS" in csv_text
    assert len(csv_text) > 1000

