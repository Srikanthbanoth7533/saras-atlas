"""
SARAS ATLAS — Phase 2 Frontend & Backend Integration Test Suite.
Validates end-to-end contract compatibility between Next.js and FastAPI,
verifying that all 10 interface modules receive valid schemas and real calculations.
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_e2e_health_and_telemetry():
    """Verify health endpoint provides telemetry for Header.tsx."""
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "HEALTHY"
    assert "SQLite WAL" in data["database"]
    assert "OR-Tools SCIP" in data["optimizer"]
    assert data["memory"]["process_working_set_mb"] > 0
    print("  [PASS] Health & Telemetry Endpoint OK")


def test_e2e_digital_twin_and_topology():
    """Verify topology endpoint provides nodes and edges for NetworkTopology.tsx."""
    resp = client.get("/api/v1/twin/topology")
    assert resp.status_code == 200
    data = resp.json()
    assert "nodes" in data and len(data["nodes"]) >= 5
    assert "edges" in data and len(data["edges"]) >= 3
    assert data["organization"]["slug"] == "vanguard-apparel-co"
    print("  [PASS] Digital Twin Topology Endpoint OK")


def test_e2e_inventory_monitoring():
    """Verify inventory summary provides SKU positions for InventoryMonitoring.tsx."""
    resp = client.get("/api/v1/twin/inventory-summary")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_skus"] == 50
    assert data["total_on_hand_units"] > 10000
    assert len(data["items"]) == 50
    print("  [PASS] Inventory Monitoring Endpoint OK")


def test_e2e_active_risks():
    """Verify operational risk sentinels feed for RiskMonitoring.tsx."""
    resp = client.get("/api/v1/risks/active")
    assert resp.status_code == 200
    data = resp.json()
    assert data["critical_count"] >= 1
    assert any("PO-9012" in r["risk_id"] for r in data["risks"])
    print("  [PASS] Sentinel Risk Monitoring Endpoint OK")


def test_e2e_simulation_studio_sliders():
    """Verify interactive sliders (0-60d delay, 0-100% surcharge, 0-100% surge) in SimulationStudio.tsx."""
    # Test with default slider values (21 days, 28% surcharge, 45% surge)
    payload = {
        "scenario_name": "Slider Test (21d, 28%, 45%)",
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
    resp = client.post("/api/v1/scenarios/simulate", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["summary_scorecard"]["stockout_days"] == 0
    assert data["summary_scorecard"]["net_contribution_margin"] > 400000.00
    assert len(data["daily_timeseries"]["revenue"]) == 90
    print("  [PASS] Simulation Studio Slider Integration OK (0 Stockout Days)")


def test_e2e_scenario_comparison():
    """Verify before-versus-after comparison for ScenarioComparison.tsx."""
    base_payload = {
        "scenario_name": "Unmitigated",
        "horizon_days": 90,
        "shocks": {
            "supplier_delays": [{"po_number": "PO-9012", "delay_days": 21}],
            "freight_surcharges": [{"lane_id": "lane_east_coast_parcel", "surcharge_percentage": 0.28}],
            "demand_elasticities": [{"sku_code": "APEX-JKT", "demand_multiplier": 1.45, "duration_days": 30}]
        },
        "mitigations": {}
    }
    mit_payload = {
        "scenario_name": "Mitigated Optimal",
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
    resp = client.post("/api/v1/scenarios/compare", json={"baseline_request": base_payload, "mitigated_request": mit_payload})
    assert resp.status_code == 200
    data = resp.json()
    assert data["stockout_days_saved"] >= 8
    assert data["net_margin_delta"] > 150000.00
    assert "protects" in data["executive_verdict"]
    print("  [PASS] Scenario Comparison Endpoint OK")


def test_e2e_prescriptive_optimization():
    """Verify OR-Tools solver execution for OptimizationRecommendations.tsx."""
    opt_payload = {
        "capital_budget_ceiling": 40000.00,
        "min_service_fill_rate": 0.95,
        "max_ad_throttle_pct": 0.35,
        "target_sku": "APEX-JKT",
        "objective": "MAXIMIZE_CONTRIBUTION_MARGIN"
    }
    resp = client.post("/api/v1/optimization/solve", json=opt_payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "OPTIMAL"
    assert data["capital_required"] <= 40000.00
    assert data["recommended_air_freight_units"] >= 500
    assert data["projected_stockout_days"] == 0
    print("  [PASS] Prescriptive Optimization Solver OK")


def test_e2e_governance_and_two_man_rule():
    """Verify Two-Man Rule rejection and valid SHA-256 seal for GovernanceInterface.tsx."""
    # 1. Two-Man Rule Violation (same ID)
    bad_req = {
        "approver_primary_id": "USR-COO-01",
        "approver_primary_name": "Elena Rostova",
        "approver_secondary_id": "USR-COO-01",
        "approver_secondary_name": "Elena Rostova",
        "decision": "APPROVED",
        "approved_capital_outlay": 20670.00
    }
    bad_resp = client.post("/api/v1/governance/approve", json=bad_req)
    assert bad_resp.status_code == 400

    # 2. Valid Two-Man Sign-off
    valid_req = {
        "approver_primary_id": "USR-COO-01",
        "approver_primary_name": "Elena Rostova (COO)",
        "approver_secondary_id": "USR-CFO-01",
        "approver_secondary_name": "Marcus Vance (CFO)",
        "decision": "APPROVED",
        "notes": "Approved emergency air freight and ground transfer for Apex Jacket disruption.",
        "approved_capital_outlay": 20670.00
    }
    valid_resp = client.post("/api/v1/governance/approve", json=valid_req)
    assert valid_resp.status_code == 200
    valid_data = valid_resp.json()
    assert valid_data["two_man_rule_satisfied"] is True
    assert len(valid_data["digital_signature_sha256"]) == 64

    # 3. Audit trail query
    audit_resp = client.get("/api/v1/governance/audit-trail")
    assert audit_resp.status_code == 200
    print("  [PASS] Two-Man Rule & Cryptographic Audit Seal OK")


def test_nextjs_build_artifacts():
    """Verify Next.js production build output exists on disk."""
    next_dir = PROJECT_ROOT / "frontend" / ".next"
    assert next_dir.exists(), "frontend/.next directory must exist after build"
    assert (next_dir / "BUILD_ID").exists(), "frontend/.next/BUILD_ID must exist"
    print("  [PASS] Next.js Production Build Artifacts Verified")


def main():
    print("=" * 70)
    print(" SARAS ATLAS — PHASE 2 INTEGRATION & QUALITY ASSURANCE SUITE")
    print("=" * 70)

    test_e2e_health_and_telemetry()
    test_e2e_digital_twin_and_topology()
    test_e2e_inventory_monitoring()
    test_e2e_active_risks()
    test_e2e_simulation_studio_sliders()
    test_e2e_scenario_comparison()
    test_e2e_prescriptive_optimization()
    test_e2e_governance_and_two_man_rule()
    test_nextjs_build_artifacts()

    print("\n" + "=" * 70)
    print(" ALL PHASE 2 INTEGRATION & FRONTEND CHECKS: PASSED (100%)")
    print("=" * 70)


if __name__ == "__main__":
    main()
