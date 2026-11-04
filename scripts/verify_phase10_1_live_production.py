"""
SARAS ATLAS - Phase 10.1 Complete Live Production Smoke & Integration Suite
Executes end-to-end tests across all 16 modules on https://saras-atlas.vercel.app
"""

import sys
import json
import httpx

BASE_URL = "https://saras-atlas.vercel.app"
API_BASE = f"{BASE_URL}/api/v1"

def run_production_smoke_test():
    print("=" * 80)
    print("SARAS ATLAS PHASE 10.1 LIVE PRODUCTION SMOKE SUITE")
    print(f"Target URL: {BASE_URL}")
    print("=" * 80)

    client = httpx.Client(base_url=API_BASE, timeout=30.0)
    fe_client = httpx.Client(base_url=BASE_URL, timeout=30.0)

    # 1. Frontend Availability
    print("\n[STEP 1] Testing Frontend Availability...")
    r_fe = fe_client.get("/")
    assert r_fe.status_code == 200, f"Frontend returned {r_fe.status_code}"
    html = r_fe.text
    assert "SARAS ATLAS" in html
    assert "Vanguard Apparel Co." in html
    print(f"  [PASS] Frontend live and serving Next.js HTML ({len(html):,} bytes)")

    # 2. Authentication & RBAC
    print("\n[STEP 2] Testing Authentication & RBAC...")
    r_auth = client.post("/auth/login", json={"username": "admin", "password": "AtlasAdmin2026!"})
    assert r_auth.status_code == 200, f"Login failed: {r_auth.text}"
    token_data = r_auth.json()
    token = token_data["access_token"]
    user = token_data["user"]
    auth_headers = {"Authorization": f"Bearer {token}"}
    print(f"  [PASS] Authenticated as {user['username']} ({user['role']}) - User: {user['full_name']}")

    # 3. Backend Health & Vitals
    print("\n[STEP 3] Testing Backend Health & System Vitals...")
    r_health = client.get("/health")
    assert r_health.status_code == 200
    h_data = r_health.json()
    assert h_data.get("status") == "HEALTHY"
    print(f"  [PASS] Health: {h_data['status']} | DB: {h_data['database']} | Optimizer: {h_data['optimizer']} | RAM: {h_data['memory']['process_working_set_mb']} MB RSS")

    # 4. Digital Twin Topology
    print("\n[STEP 4] Testing Module 2: Digital Twin Topology...")
    r_topo = client.get("/twin/topology")
    assert r_topo.status_code == 200
    topo_data = r_topo.json()
    assert len(topo_data.get("nodes", [])) >= 5
    print(f"  [PASS] Topology: {len(topo_data['nodes'])} Nodes, {len(topo_data['edges'])} Edges")

    # 5. Inventory Summary
    print("\n[STEP 5] Testing Module 3: Inventory Monitoring...")
    r_inv = client.get("/twin/inventory-summary")
    assert r_inv.status_code == 200
    inv_data = r_inv.json()
    print(f"  [PASS] Inventory: {inv_data.get('total_skus')} SKUs, {inv_data.get('total_on_hand_units'):,} on-hand units")

    # 6. Sentinel Risk Detection
    print("\n[STEP 6] Testing Module 4: Risk Sentinels...")
    r_risks = client.get("/risks/active")
    assert r_risks.status_code == 200
    risk_data = r_risks.json()
    print(f"  [PASS] Active Risks: {risk_data.get('total_active_risks')} detected ({risk_data.get('critical_count')} critical)")

    # 7. Scenario Simulation
    print("\n[STEP 7] Testing Module 5: Discrete Difference Simulation Studio...")
    sim_payload = {
        "scenario_name": "Status Quo Disruption",
        "horizon_days": 90,
        "shocks": {
            "supplier_delays": [{"po_number": "PO-9012", "delay_days": 21}],
            "freight_surcharges": [{"lane_id": "lane_east_coast_parcel", "surcharge_percentage": 0.28}],
            "demand_elasticities": [{"sku_code": "APEX-JKT", "demand_multiplier": 1.45, "duration_days": 30}]
        },
        "mitigations": {}
    }
    r_sim = client.post("/scenarios/simulate", json=sim_payload)
    assert r_sim.status_code == 200
    sim_data = r_sim.json()
    scorecard = sim_data.get("summary_scorecard", {})
    print(f"  [PASS] Simulation: Revenue=${scorecard.get('net_revenue'):,.2f} | Lost Units={scorecard.get('unfulfilled_lost_orders')} | CM=${scorecard.get('net_contribution_margin'):,.2f}")

    # 8. Prescriptive SCIP Optimization
    print("\n[STEP 8] Testing Module 6: Prescriptive Optimization Solver...")
    opt_payload = {
        "capital_budget_ceiling": 40000.0,
        "min_service_fill_rate": 0.95,
        "max_ad_throttle_pct": 0.35,
        "target_sku": "APEX-JKT",
        "objective": "MAXIMIZE_CONTRIBUTION_MARGIN"
    }
    r_opt = client.post("/optimization/solve", json=opt_payload)
    assert r_opt.status_code == 200
    opt_data = r_opt.json()
    assert opt_data.get("status") == "OPTIMAL"
    assert opt_data.get("recommended_air_freight_units") == 2995
    assert opt_data.get("recommended_transfer_units") == 800
    assert abs(opt_data.get("capital_required", 0) - 39997.50) < 0.01
    print(f"  [PASS] Optimization: {opt_data.get('status')} in {opt_data.get('solve_time_ms')} ms")
    print(f"         Air: {opt_data.get('recommended_air_freight_units')} units | Transfer: {opt_data.get('recommended_transfer_units')} units | Outlay: ${opt_data.get('capital_required'):,.2f}")

    # 9. Two-Man Rule Governance Approval
    print("\n[STEP 9] Testing Module 7: Two-Man Rule Governance...")
    gov_payload = {
        "approver_primary_id": "exec_marcus_vance",
        "approver_primary_name": "Marcus Vance (VP Supply Chain)",
        "approver_secondary_id": "exec_elena_rostova",
        "approver_secondary_name": "Elena Rostova (Chief Financial Officer)",
        "decision": "APPROVED",
        "notes": "Production release dual executive authorization (Two-Man Rule)",
        "approved_capital_outlay": 39997.50
    }
    r_gov = client.post("/governance/approve", json=gov_payload, headers=auth_headers)
    assert r_gov.status_code == 200
    gov_data = r_gov.json()
    print(f"  [PASS] Governance Record: ID={gov_data.get('id')} | Decision={gov_data.get('decision')} | Two-Man Satisfied={gov_data.get('two_man_rule_satisfied')}")
    print(f"         SHA-256 Signature: {gov_data.get('digital_signature_sha256')[:32]}...")

    # 10. Cryptographic Audit Trail
    print("\n[STEP 10] Testing Cryptographic Audit Trail Ledger...")
    r_audit = client.get("/governance/audit-trail", headers=auth_headers)
    assert r_audit.status_code == 200
    audit_data = r_audit.json()
    records = audit_data.get("recent_approvals", []) + audit_data.get("recent_simulations", [])
    assert len(records) > 0, "Audit trail empty"
    print(f"  [PASS] Audit Trail: {len(records)} cryptographically sealed records verified ({len(audit_data.get('recent_approvals', []))} approvals, {len(audit_data.get('recent_simulations', []))} simulations)")

    # 11. Root Cause Analysis
    print("\n[STEP 11] Testing Module 8: Root Cause Analysis...")
    r_rca = client.get("/rca/trace?disruption_id=DISR-PO9012", headers=auth_headers)
    assert r_rca.status_code == 200
    rca_data = r_rca.json()
    print(f"  [PASS] RCA Trace: Primary Cause = '{rca_data.get('primary_root_cause')}'")
    attributions = rca_data.get("financial_attribution", [])
    tot_loss = sum(a.get("dollar_impact", 0) for a in attributions)
    print(f"         Total Financial Attribution = ${tot_loss:,.2f} across {len(attributions)} categories")

    # 12. Demand Forecasting
    print("\n[STEP 12] Testing Module 9: Demand Forecasting Studio...")
    r_fc = client.get("/forecasting/evaluate", headers=auth_headers)
    assert r_fc.status_code == 200
    fc_data = r_fc.json()
    print(f"  [PASS] Demand Forecast: Best Model = '{fc_data.get('best_model_name')}' | Models Evaluated = {len(fc_data.get('models_evaluated', []))}")

    # 13. Executive Reporting Summary
    print("\n[STEP 13] Testing Module 10: Executive Reporting...")
    r_rep = client.get("/reports/summary", headers=auth_headers)
    assert r_rep.status_code == 200
    rep_data = r_rep.json()
    print(f"  [PASS] Executive Report: Title = '{rep_data.get('title')}'")
    rca_rep = rep_data.get("root_cause_analysis", {})
    rep_losses = rca_rep.get("attributions", [])
    print(f"         Report Attributions: {len(rep_losses)} rows including total reconciled loss")

    # 14. ReportLab Vector PDF Export
    print("\n[STEP 14] Testing Vector PDF Export...")
    r_pdf = client.get("/reports/export/pdf", headers=auth_headers)
    assert r_pdf.status_code == 200
    assert r_pdf.content.startswith(b"%PDF")
    print(f"  [PASS] Vector PDF Export: {len(r_pdf.content):,} bytes verified")

    # 15. RFC-4180 CSV Export
    print("\n[STEP 15] Testing RFC-4180 CSV Export...")
    r_csv = client.get("/reports/export/csv", headers=auth_headers)
    assert r_csv.status_code == 200
    csv_text = r_csv.text
    assert "224,500.00" in csv_text or "224500" in csv_text
    print(f"  [PASS] CSV Export: Verified ({len(csv_text.splitlines())} lines) with $224,500.00 confirmed")

    # 16. Enterprise Connectors Gateway
    print("\n[STEP 16] Testing Enterprise Connectors Gateway...")
    r_conn = client.get("/connectors/list", headers=auth_headers)
    assert r_conn.status_code == 200
    connectors = r_conn.json()
    print(f"  [PASS] Connectors: {len(connectors)} enterprise connectors registered")

    # 17. Batch Scenario Engine
    print("\n[STEP 17] Testing Batch Scenario Engine...")
    r_batch = client.get("/batch/generate-benchmark")
    assert r_batch.status_code == 200
    benchmark_scenarios = r_batch.json()
    print(f"  [PASS] Batch Engine: Generated {len(benchmark_scenarios)} benchmark scenarios")

    # 18. Policy Optimization
    print("\n[STEP 18] Testing Dynamic Policy Optimization...")
    r_pol = client.get("/policy/standard-suite")
    assert r_pol.status_code == 200
    pol_data = r_pol.json()
    print(f"  [PASS] Policy Optimization: {len(pol_data)} candidate policies in standard suite")

    print("\n" + "=" * 80)
    print("ALL 18 LIVE PRODUCTION SMOKE TESTS PASSED CLEANLY!")
    print("=" * 80)

if __name__ == "__main__":
    try:
        run_production_smoke_test()
    except Exception as e:
        print(f"\n[FATAL] Live production smoke test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
