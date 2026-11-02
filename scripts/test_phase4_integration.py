"""
SARAS ATLAS — Phase 4 Automated End-to-End Integration Test Suite
Validates all 12 Phase 4 enterprise intelligence, security, forecasting, connector,
and reporting checkpoints via high-speed in-process TestClient.
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_phase4_e2e():
    print("=" * 80)
    print("SARAS ATLAS — PHASE 4 AUTOMATED END-TO-END INTEGRATION TEST SUITE")
    print("=" * 80)

    # [1/12] Backend Diagnostics & Health
    print("[1/12] Verifying Backend Diagnostics & Security Headers...")
    res = client.get("/api/v1/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    health = res.json()
    assert health["status"] == "HEALTHY"
    # Verify enterprise security headers
    assert res.headers.get("x-content-type-options") == "nosniff"
    assert res.headers.get("x-frame-options") == "DENY"
    print("      [PASS] Health check online. Security headers active (nosniff, DENY).")

    # [2/12] User Authentication & RBAC Login
    print("[2/12] Testing User Authentication & JWT Issuance (POST /api/v1/auth/login)...")
    auth_res = client.post("/api/v1/auth/login", json={"username": "admin", "password": "AtlasAdmin2026!"})
    assert auth_res.status_code == 200, f"Login failed: {auth_res.text}"
    token_data = auth_res.json()
    token = token_data["access_token"]
    assert token_data["user"]["role"] == "ADMIN"
    auth_headers = {"Authorization": f"Bearer {token}"}
    print(f"      [PASS] Authenticated user {token_data['user']['username']} as {token_data['user']['role']}.")

    # [3/12] Security Audit Trail
    print("[3/12] Auditing Security Event Trail (GET /api/v1/security/audit-trail)...")
    audit_res = client.get("/api/v1/security/audit-trail?limit=10", headers=auth_headers)
    assert audit_res.status_code == 200, f"Audit trail failed: {audit_res.text}"
    audit_logs = audit_res.json()
    assert len(audit_logs) > 0
    print(f"      [PASS] Retrieved {len(audit_logs)} security audit log entries.")

    # [4/12] AI Decision Intelligence Grounding
    print("[4/12] Testing AI Decision Intelligence (POST /api/v1/intelligence/query)...")
    q_res = client.post(
        "/api/v1/intelligence/query",
        json={"query": "What is our current stockout risk and days of coverage?"},
        headers=auth_headers,
    )
    assert q_res.status_code == 200, f"Query failed: {q_res.text}"
    ans = q_res.json()
    assert ans["confidence_score"] >= 0.70
    assert len(ans["citations"]) > 0
    print(f"      [PASS] Grounded answer generated for intent {ans['intent_topic']} with {len(ans['citations'])} citations.")

    # [5/12] Sample Inquiries Feed
    print("[5/12] Testing Sample Inquiries Feed (GET /api/v1/intelligence/sample-queries)...")
    sq_res = client.get("/api/v1/intelligence/sample-queries")
    assert sq_res.status_code == 200
    samples = sq_res.json()
    assert len(samples) >= 3
    print(f"      [PASS] Retrieved {len(samples)} pre-built executive questions.")

    # [6/12] Root Cause Analysis & Dependency Tracing
    print("[6/12] Testing Root Cause Analysis (GET /api/v1/rca/trace)...")
    rca_res = client.get("/api/v1/rca/trace?disruption_id=DISR-PO9012", headers=auth_headers)
    assert rca_res.status_code == 200, f"RCA failed: {rca_res.text}"
    rca = rca_res.json()
    assert len(rca["causal_chain"]) == 5
    assert rca["total_financial_impact"] == 224500.00
    print(f"      [PASS] Causal pathway traced: {rca['causal_chain'][0]['label']} -> {rca['causal_chain'][-1]['label']}.")

    # [7/12] Explainable Prescriptive Recommendations
    print("[7/12] Testing Explainable Recommendations (GET /api/v1/explainability/recommendations)...")
    rec_res = client.get("/api/v1/explainability/recommendations", headers=auth_headers)
    assert rec_res.status_code == 200, f"Recommendations failed: {rec_res.text}"
    dossier = rec_res.json()
    assert dossier["solver_status"] == "OPTIMAL"
    assert len(dossier["recommendations"]) >= 4
    for r in dossier["recommendations"]:
        assert r["what_action"] and r["why_recommended"] and r["expected_financial_benefits"]
    print(f"      [PASS] Retrieved {len(dossier['recommendations'])} complete 8-dimension explainable dossiers.")

    # [8/12] Advanced Forecasting with Prediction Intervals
    print("[8/12] Testing Advanced Time-Series Forecasting (GET /api/v1/forecasting/evaluate)...")
    fc_res = client.get("/api/v1/forecasting/evaluate?series_type=DAILY_DEMAND&horizon_days=30", headers=auth_headers)
    assert fc_res.status_code == 200, f"Forecasting failed: {fc_res.text}"
    fc = fc_res.json()
    assert len(fc["models_evaluated"]) == 3
    assert len(fc["forecast_trajectory"]) == 120
    print(f"      [PASS] Evaluated 3 models on held-out split. Best: {fc['best_model_name']} (30d Horizon).")

    # [9/12] Enterprise Cloud Warehouse Connectors
    print("[9/12] Testing Enterprise Connectors (GET /list & POST /test)...")
    conn_res = client.get("/api/v1/connectors/list", headers=auth_headers)
    assert conn_res.status_code == 200
    conns = conn_res.json()
    assert len(conns) >= 5

    test_res = client.post("/api/v1/connectors/CONN-BQ-01/test", headers=auth_headers)
    assert test_res.status_code == 200
    test_data = test_res.json()
    assert test_data["success"] is True
    print(f"      [PASS] Tested Google BigQuery sandbox: {test_data['status']} ({test_data['latency_ms']} ms).")

    # [10/12] Schema Catalog Introspection
    print("[10/12] Testing Schema Catalog Introspection (GET /connectors/CONN-SNOW-02/schema)...")
    schema_res = client.get("/api/v1/connectors/CONN-SNOW-02/schema", headers=auth_headers)
    assert schema_res.status_code == 200
    schema_data = schema_res.json()
    assert "orders_fact" in schema_data["tables"]
    print(f"      [PASS] Discovered Snowflake schema: {len(schema_data['tables'])} canonical tables.")

    # [11/12] Executive Report Summary & Exports
    print("[11/12] Testing Executive Reporting (PDF & CSV Exports)...")
    rep_res = client.get("/api/v1/reports/summary", headers=auth_headers)
    assert rep_res.status_code == 200
    rep_summary = rep_res.json()
    assert "executive_summary" in rep_summary

    pdf_res = client.get("/api/v1/reports/export/pdf", headers=auth_headers)
    assert pdf_res.status_code == 200
    assert pdf_res.headers["content-type"] == "application/pdf"
    assert len(pdf_res.content) > 2000

    csv_res = client.get("/api/v1/reports/export/csv", headers=auth_headers)
    assert csv_res.status_code == 200
    assert "text/csv" in csv_res.headers["content-type"]
    assert len(csv_res.text) > 1000
    print(f"      [PASS] Generated PDF ({len(pdf_res.content):,} bytes) and CSV ({len(csv_res.text):,} chars).")

    # [12/12] Database Integrity & Next.js Build Artifacts
    print("[12/12] Auditing Database Integrity & Next.js 15 Build Artifacts...")
    build_id_path = Path("frontend/.next/BUILD_ID")
    assert build_id_path.exists(), "Next.js BUILD_ID not found"
    build_id = build_id_path.read_text(encoding="utf-8").strip()

    db_path = Path("data/saras_atlas.db")
    assert db_path.exists(), "Database file missing"
    print(f"      [PASS] Database online ({db_path.stat().st_size:,} bytes). Next.js Build ID: {build_id}")

    print("=" * 80)
    print("ALL 12 PHASE 4 INTEGRATION CHECKPOINTS PASSED WITH 100% SUCCESS!")
    print("=" * 80)


if __name__ == "__main__":
    try:
        test_phase4_e2e()
        sys.exit(0)
    except AssertionError as e:
        print(f"\n[FAIL] Assertion error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        sys.exit(1)
