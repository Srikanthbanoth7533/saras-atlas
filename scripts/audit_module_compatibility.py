"""
SARAS ATLAS - Comprehensive Frontend-to-Backend Compatibility Audit
Audits all 16 platform modules against live production backend on https://saras-atlas.vercel.app
"""

import sys
import json
import httpx

BASE_URL = "https://saras-atlas.vercel.app"
API_BASE = f"{BASE_URL}/api/v1"

def audit_compatibility():
    print("=" * 80)
    print("SARAS ATLAS PHASE 10.2: BACKEND COMPATIBILITY AUDIT")
    print(f"Target URL: {BASE_URL}")
    print("=" * 80)

    client = httpx.Client(base_url=API_BASE, timeout=30.0)

    # Authenticate
    r_auth = client.post("/auth/login", json={"username": "admin", "password": "AtlasAdmin2026!"})
    token = r_auth.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    modules = [
        ("Module 1: Situation Room / Vitals", "GET", "/health", None, False, lambda d: d.get("status") == "HEALTHY"),
        ("Module 2: Digital Twin Topology", "GET", "/twin/topology", None, False, lambda d: len(d.get("nodes", [])) >= 5),
        ("Module 3: Inventory Monitoring", "GET", "/twin/inventory-summary", None, False, lambda d: d.get("total_skus") == 50),
        ("Module 4: Risk Sentinels", "GET", "/risks/active", None, False, lambda d: d.get("status") == "SCANNED"),
        ("Module 5: Scenario Simulation", "POST", "/scenarios/simulate", {
            "scenario_name": "Test Simulation",
            "horizon_days": 90,
            "shocks": {"supplier_delays": [{"po_number": "PO-9012", "delay_days": 21}]},
            "mitigations": {}
        }, False, lambda d: "summary_scorecard" in d),
        ("Module 6: SCIP Prescriptive Optimizer", "POST", "/optimization/solve", {
            "capital_budget_ceiling": 40000.0,
            "min_service_fill_rate": 0.95,
            "max_ad_throttle_pct": 0.35,
            "target_sku": "APEX-JKT",
            "objective": "MAXIMIZE_CONTRIBUTION_MARGIN"
        }, False, lambda d: d.get("status") == "OPTIMAL" and d.get("recommended_air_freight_units") == 2995 and d.get("recommended_transfer_units") == 800),
        ("Module 7: Financial Waterfall Bridge", "GET", "/reports/summary", None, True, lambda d: "root_cause_analysis" in d),
        ("Module 8: Two-Man Rule Governance", "POST", "/governance/approve", {
            "approver_primary_id": "exec_marcus_vance",
            "approver_primary_name": "Marcus Vance (VP Supply Chain)",
            "approver_secondary_id": "exec_elena_rostova",
            "approver_secondary_name": "Elena Rostova (Chief Financial Officer)",
            "decision": "APPROVED",
            "notes": "Compatibility audit test",
            "approved_capital_outlay": 39997.50
        }, True, lambda d: d.get("two_man_rule_satisfied") is True and len(d.get("digital_signature_sha256", "")) == 64),
        ("Module 9: Audit Trail Ledger", "GET", "/governance/audit-trail", None, True, lambda d: d.get("total_approvals_recorded", 0) > 0),
        ("Module 10: Root Cause Analysis (RCA)", "GET", "/rca/trace?disruption_id=DISR-PO9012", None, True, lambda d: d.get("total_financial_impact") == 224500.0),
        ("Module 11: Demand Forecasting Studio", "GET", "/forecasting/evaluate", None, True, lambda d: len(d.get("models_evaluated", [])) >= 3),
        ("Module 12: Executive Reporting Summary", "GET", "/reports/summary", None, True, lambda d: len(d.get("kpi_posture", [])) >= 5),
        ("Module 13: ReportLab Vector PDF Export", "GET", "/reports/export/pdf", None, True, lambda raw: raw.startswith(b"%PDF")),
        ("Module 14: RFC-4180 CSV Export", "GET", "/reports/export/csv", None, True, lambda text: "224,500.00" in text or "224500" in text),
        ("Module 15: Enterprise Data Ingestion", "GET", "/ingestion/quality", None, False, lambda d: d.get("overall_health_score") >= 90.0),
        ("Module 16: Enterprise Connectors Gateway", "GET", "/connectors/list", None, True, lambda d: len(d) >= 5),
    ]

    passed = 0
    failed = 0

    print(f"\nEvaluating compatibility across all {len(modules)} core modules:")
    for name, method, endpoint, payload, use_auth, validator in modules:
        try:
            req_headers = headers if use_auth else {}
            if method == "GET":
                resp = client.get(endpoint, headers=req_headers)
            else:
                resp = client.post(endpoint, json=payload, headers=req_headers)

            assert resp.status_code == 200, f"HTTP {resp.status_code}: {resp.text[:100]}"

            if "pdf" in endpoint:
                valid = validator(resp.content)
            elif "csv" in endpoint:
                valid = validator(resp.text)
            else:
                valid = validator(resp.json())

            assert valid, "Validator assertion failed"
            print(f"  [COMPATIBLE] {name}: HTTP {resp.status_code} OK")
            passed += 1
        except Exception as e:
            print(f"  [INCOMPATIBLE] {name}: {e}")
            failed += 1

    print("\n" + "=" * 80)
    print(f"AUDIT SUMMARY: {passed}/{len(modules)} Modules Fully Compatible | {failed} Incompatible")
    print("=" * 80)
    return failed == 0

if __name__ == "__main__":
    success = audit_compatibility()
    sys.exit(0 if success else 1)
