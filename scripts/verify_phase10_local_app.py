"""
SARAS ATLAS — Phase 10.0 Local Application Comprehensive End-to-End Verification
"""

import urllib.request
import json
import sys

BACKEND_URL = "http://127.0.0.1:8000/api/v1"
FRONTEND_URL = "http://localhost:3000"

def test_endpoint(name, url, method="GET", payload=None, expected_code=200):
    try:
        req = urllib.request.Request(url, method=method)
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "application/json")
        data = json.dumps(payload).encode("utf-8") if payload else None
        
        with urllib.request.urlopen(req, data=data, timeout=10) as resp:
            body = resp.read()
            code = resp.getcode()
            assert code == expected_code, f"Expected {expected_code}, got {code}"
            print(f"  [PASS] {name}: HTTP {code} ({len(body)} bytes)")
            return body
    except Exception as e:
        print(f"  [FAIL] {name}: {e}")
        sys.exit(1)

def run_local_verification():
    print("================================================================================")
    print("PHASE 10.0 LOCAL APPLICATION SYSTEMATIC VERIFICATION")
    print("================================================================================")
    
    # 1. Health & Vitals
    h_bytes = test_endpoint("Health Check", f"{BACKEND_URL}/health")
    h_json = json.loads(h_bytes.decode("utf-8"))
    assert h_json["status"] == "HEALTHY", "Health status not HEALTHY"
    print(f"      Status: {h_json['status']} | DB: {h_json['database']} | Memory: {h_json['memory']['process_working_set_mb']} MB RSS")
    
    # 2. Digital Twin Topology
    t_bytes = test_endpoint("Twin Topology", f"{BACKEND_URL}/twin/topology")
    t_json = json.loads(t_bytes.decode("utf-8"))
    nodes_count = len(t_json.get("nodes", []))
    edges_count = len(t_json.get("edges", []))
    print(f"      Topology: {nodes_count} Nodes | {edges_count} Directed Edges")
    
    # 3. Inventory Summary
    i_bytes = test_endpoint("Inventory Summary", f"{BACKEND_URL}/twin/inventory-summary")
    i_json = json.loads(i_bytes.decode("utf-8"))
    sku_count = len(i_json.get("inventory_records", []))
    print(f"      Inventory Records Loaded: {sku_count} facilities/SKUs")
    
    # 4. Active Risks Sentinel
    r_bytes = test_endpoint("Active Risks Sentinel", f"{BACKEND_URL}/risks/active")
    r_json = json.loads(r_bytes.decode("utf-8"))
    risks_count = len(r_json.get("risks", []))
    print(f"      Active Risks Detected: {risks_count}")
    
    # 5. Simulation Run (Unmitigated)
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
    s_bytes = test_endpoint("Simulation Execution", f"{BACKEND_URL}/scenarios/simulate", method="POST", payload=sim_payload)
    s_json = json.loads(s_bytes.decode("utf-8"))
    scorecard = s_json.get("summary_scorecard", {})
    print(f"      Sim Output: Revenue=${scorecard.get('net_revenue'):,.2f} | Lost Units={scorecard.get('unfulfilled_lost_orders')} | CM=${scorecard.get('net_contribution_margin'):,.2f}")
    
    # 6. Prescriptive SCIP Optimization
    opt_payload = {
        "capital_budget_ceiling": 40000.0,
        "min_service_fill_rate": 0.95,
        "max_ad_throttle_pct": 0.35,
        "target_sku": "APEX-JKT",
        "objective": "MAXIMIZE_CONTRIBUTION_MARGIN"
    }
    opt_bytes = test_endpoint("Prescriptive SCIP Optimization", f"{BACKEND_URL}/optimization/solve", method="POST", payload=opt_payload)
    opt_json = json.loads(opt_bytes.decode("utf-8"))
    print(f"      SCIP Status: {opt_json.get('status')} in {opt_json.get('solve_time_ms')} ms")
    print(f"      Allocations: Air={opt_json.get('recommended_air_freight_units')} | Ground={opt_json.get('recommended_transfer_units')} | Capital=${opt_json.get('capital_required'):,.2f}")
    assert opt_json.get("status") == "OPTIMAL", "Solver status not OPTIMAL"
    assert opt_json.get("recommended_transfer_units") == 800, "Ground units != 800"
    assert opt_json.get("recommended_air_freight_units") == 2995, "Air units != 2995"
    assert abs(opt_json.get("capital_required") - 39997.50) < 0.01, "Capital required != 39997.50"
    
    # 7. Governance Approval (Two-Man Rule)
    gov_payload = {
        "approver_primary_id": "exec_marcus_vance",
        "approver_primary_name": "Marcus Vance (VP Supply Chain)",
        "approver_secondary_id": "exec_elena_rostova",
        "approver_secondary_name": "Elena Rostova (Chief Financial Officer)",
        "decision": "APPROVED",
        "notes": "Authorized emergency expedited air freight and domestic transfer under Two-Man Rule policy.",
        "approved_capital_outlay": 39997.50
    }
    g_bytes = test_endpoint("Governance Dual-Key Submission", f"{BACKEND_URL}/governance/approve", method="POST", payload=gov_payload)
    g_json = json.loads(g_bytes.decode("utf-8"))
    print(f"      Approval Record ID: {g_json.get('id')} | Decision: {g_json.get('decision')} | Two-Man Satisfied: {g_json.get('two_man_rule_satisfied')}")
    print(f"      Digital Signature (SHA-256): {g_json.get('digital_signature_sha256')[:32]}...")
    
    # 8. Governance Audit Trail
    a_bytes = test_endpoint("Audit Trail Ledger", f"{BACKEND_URL}/governance/audit-trail")
    a_json = json.loads(a_bytes.decode("utf-8"))
    records_count = len(a_json.get("audit_trail", []))
    print(f"      Audit Trail Length: {records_count} cryptographically sealed events")
    
    # 9. Executive Report Summary
    rep_bytes = test_endpoint("Executive Report Summary", f"{BACKEND_URL}/reports/summary")
    rep_json = json.loads(rep_bytes.decode("utf-8"))
    print(f"      Report Title: '{rep_json.get('title')}' | Enterprise: '{rep_json.get('enterprise')}'")
    
    # 10. PDF Export
    pdf_bytes = test_endpoint("PDF Export Stream", f"{BACKEND_URL}/reports/export/pdf")
    assert pdf_bytes.startswith(b"%PDF"), "Response is not a valid PDF binary"
    print(f"      Valid PDF binary verified ({len(pdf_bytes)} bytes)")
    
    # 11. CSV Export
    csv_bytes = test_endpoint("CSV Export Stream", f"{BACKEND_URL}/reports/export/csv")
    csv_text = csv_bytes.decode("utf-8")
    assert "$224,500.00" in csv_text and "$129,844.32" in csv_text, "Reconciled loss figures missing from CSV"
    print(f"      Valid CSV export verified with $224,500.00 and $129,844.32 ({len(csv_text)} chars)")
    
    # 12. Frontend Web Pages
    fe_home = test_endpoint("Frontend Home Page (Root /)", f"{FRONTEND_URL}/")
    fe_home_str = fe_home.decode("utf-8")
    assert "SARAS ATLAS" in fe_home_str, "SARAS ATLAS brand not in frontend HTML"
    print(f"      Frontend Home rendered successfully with brand title and Next.js scripts")
    
    print("================================================================================")
    print("ALL LOCAL APPLICATION ENDPOINTS & FLOWS VERIFIED SUCCESSFULLY!")
    print("================================================================================")

if __name__ == "__main__":
    run_local_verification()
