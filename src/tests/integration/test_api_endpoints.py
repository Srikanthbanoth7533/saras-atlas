"""
SARAS ATLAS — Integration Tests for FastAPI REST Endpoints.
Uses httpx.AsyncClient with ASGITransport to test all API routes in-process.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from src.api.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_health_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "HEALTHY"
        assert "SQLite WAL" in data["database"]
        assert "OR-Tools SCIP" in data["optimizer"]
        assert "system_total_phys_gb" in data["memory"]
        assert data["memory"]["process_working_set_mb"] > 0


@pytest.mark.anyio
async def test_twin_topology_and_inventory_endpoints():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Topology
        top_resp = await client.get("/api/v1/twin/topology")
        assert top_resp.status_code == 200
        top_data = top_resp.json()
        assert top_data["organization"]["slug"] == "vanguard-apparel-co"
        assert len(top_data["nodes"]) >= 5
        assert len(top_data["edges"]) >= 3

        # Inventory Summary
        inv_resp = await client.get("/api/v1/twin/inventory-summary")
        assert inv_resp.status_code == 200
        inv_data = inv_resp.json()
        assert inv_data["total_skus"] == 50
        assert inv_data["total_on_hand_units"] > 10000


@pytest.mark.anyio
async def test_active_risks_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        risk_resp = await client.get("/api/v1/risks/active")
        assert risk_resp.status_code == 200
        data = risk_resp.json()
        assert data["status"] == "SCANNED"
        assert data["critical_count"] >= 1
        # PO-9012 delay should be flagged
        po_risks = [r for r in data["risks"] if "PO-9012" in r["risk_id"]]
        assert len(po_risks) == 1
        assert po_risks[0]["severity"] == "CRITICAL"


@pytest.mark.anyio
async def test_scenario_simulate_and_compare_endpoints():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Simulate unmitigated
        unmitigated_payload = {
            "scenario_name": "API Unmitigated Test",
            "horizon_days": 90,
            "shocks": {
                "supplier_delays": [{"po_number": "PO-9012", "delay_days": 21}],
                "freight_surcharges": [{"lane_id": "lane_east_coast_parcel", "surcharge_percentage": 0.28}],
                "demand_elasticities": [{"sku_code": "APEX-JKT", "demand_multiplier": 1.45, "duration_days": 30}]
            },
            "mitigations": {}
        }
        sim_resp = await client.post("/api/v1/scenarios/simulate", json=unmitigated_payload)
        assert sim_resp.status_code == 200
        sim_data = sim_resp.json()
        assert sim_data["summary_scorecard"]["stockout_days"] >= 8
        assert sim_data["execution_duration_ms"] < 200
        assert len(sim_data["daily_timeseries"]["revenue"]) == 90

        # 2. Compare baseline vs mitigated
        mitigated_payload = {
            "scenario_name": "API Mitigated Test",
            "horizon_days": 90,
            "shocks": {
                "supplier_delays": [{"po_number": "PO-9012", "delay_days": 21}],
                "freight_surcharges": [{"lane_id": "lane_east_coast_parcel", "surcharge_percentage": 0.28}],
                "demand_elasticities": [{"sku_code": "APEX-JKT", "demand_multiplier": 1.45, "duration_days": 30}]
            },
            "mitigations": {
                "emergency_air_freight_units": 1500,
                "inter_warehouse_transfer_units": 600,
                "ad_spend_throttle_percentage": 0.18
            }
        }
        compare_payload = {
            "baseline_request": unmitigated_payload,
            "mitigated_request": mitigated_payload
        }
        comp_resp = await client.post("/api/v1/scenarios/compare", json=compare_payload)
        assert comp_resp.status_code == 200
        comp_data = comp_resp.json()
        assert comp_data["stockout_days_saved"] >= 8
        assert comp_data["net_margin_delta"] > 0.0
        assert "protects" in comp_data["executive_verdict"]


@pytest.mark.anyio
async def test_prescriptive_optimization_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        opt_payload = {
            "capital_budget_ceiling": 40000.00,
            "min_service_fill_rate": 0.95,
            "max_ad_throttle_pct": 0.35,
            "target_sku": "APEX-JKT",
            "objective": "MAXIMIZE_CONTRIBUTION_MARGIN"
        }
        opt_resp = await client.post("/api/v1/optimization/solve", json=opt_payload)
        assert opt_resp.status_code == 200
        opt_data = opt_resp.json()
        assert opt_data["status"] == "OPTIMAL"
        assert opt_data["capital_required"] <= 40000.00
        assert opt_data["projected_stockout_days"] == 0
        assert opt_data["projected_net_contribution_margin"] > 400000.00


@pytest.mark.anyio
async def test_governance_two_man_rule_and_audit_trail():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Approval with valid Two-Man Rule
        valid_approval = {
            "approver_primary_id": "USR-COO-01",
            "approver_primary_name": "Chief Operating Officer",
            "approver_secondary_id": "USR-CFO-01",
            "approver_secondary_name": "Chief Financial Officer",
            "decision": "APPROVED",
            "notes": "Authorized emergency air freight and transfer for Apex Jacket disruption.",
            "approved_capital_outlay": 20670.00
        }
        appr_resp = await client.post("/api/v1/governance/approve", json=valid_approval)
        assert appr_resp.status_code == 200
        appr_data = appr_resp.json()
        assert appr_data["two_man_rule_satisfied"] is True
        assert len(appr_data["digital_signature_sha256"]) == 64

        # 2. Rejection of single-user attempt violating Two-Man Rule
        invalid_approval = {
            "approver_primary_id": "USR-COO-01",
            "approver_primary_name": "Chief Operating Officer",
            "approver_secondary_id": "USR-COO-01",  # Same user!
            "approver_secondary_name": "Chief Operating Officer",
            "decision": "APPROVED",
            "approved_capital_outlay": 20670.00
        }
        bad_resp = await client.post("/api/v1/governance/approve", json=invalid_approval)
        assert bad_resp.status_code == 400
        assert "Two-man rule violation" in bad_resp.json()["detail"]

        # 3. Audit trail query
        audit_resp = await client.get("/api/v1/governance/audit-trail")
        assert audit_resp.status_code == 200
        audit_data = audit_resp.json()
        assert audit_data["total_approvals_recorded"] >= 1
        assert len(audit_data["recent_approvals"]) >= 1
