"""
SARAS ATLAS — Phase 3 End-to-End Integration Test Suite.
Validates Batch Simulation Engine, Sensitivity Sweeps, Dynamic Policy Optimization,
Pareto Frontiers, Supplier Sourcing, Enterprise Ingestion, Transactional Rollback,
and Next.js Build Artifacts using FastAPI TestClient.
"""

import os
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_phase3_integration():
    print("=" * 80)
    print("SARAS ATLAS — PHASE 3 AUTOMATED END-TO-END INTEGRATION TEST SUITE")
    print("=" * 80)

    # 1. Health & Vitals
    print("[1/10] Verifying Backend Health & Diagnostics...")
    r = client.get("/api/v1/health")
    assert r.status_code == 200, f"Health check failed: {r.text}"
    assert r.json().get("status") == "HEALTHY"
    print("      [PASS] FastAPI Backend is Healthy & Memory Telemetry Active.")

    # 2. Multi-Scenario Batch Simulation
    print("[2/10] Testing Multi-Scenario Batch Simulation (POST /api/v1/batch/run)...")
    bench_r = client.get("/api/v1/batch/generate-benchmark?count=10")
    assert bench_r.status_code == 200, f"Benchmark gen failed: {bench_r.text}"
    scenarios = bench_r.json()
    assert len(scenarios) == 10, f"Expected 10 scenarios, got {len(scenarios)}"

    batch_r = client.post(
        "/api/v1/batch/run",
        json={
            "batch_name": "Phase 3 Automated Test Batch",
            "scenarios": scenarios,
            "parallel": True,
            "max_workers": 4,
            "persist_results": True,
            "random_seed": 42,
        },
    )
    assert batch_r.status_code == 200, f"Batch run failed: {batch_r.text}"
    b_data = batch_r.json()
    assert b_data["completed_scenarios"] == 10
    assert b_data["best_case"]["composite_score"] >= b_data["worst_case"]["composite_score"]
    print(f"      [PASS] Batch executed 10 scenarios in {b_data['total_execution_ms']:.1f} ms "
          f"({b_data['scenarios_per_second']:.1f} scn/sec). Best: {b_data['best_case']['scenario_name'][:25]}")

    # 3. Parametric Sensitivity Analysis
    print("[3/10] Testing Parametric Sensitivity Sweep (POST /api/v1/batch/sensitivity)...")
    sens_r = client.post(
        "/api/v1/batch/sensitivity",
        json={
            "parameter": "supplier_delay",
            "min_value": 0,
            "max_value": 60,
            "steps": 7,
        },
    )
    assert sens_r.status_code == 200, f"Sensitivity sweep failed: {sens_r.text}"
    s_data = sens_r.json()
    assert s_data["steps_evaluated"] == 7
    assert len(s_data["points"]) == 7
    print(f"      [PASS] Sensitivity sweep evaluated {s_data['steps_evaluated']} points across delay (0..60d).")

    # 4. Policy Suite Retrieval
    print("[4/10] Testing Candidate Mitigation Policy Suite (GET /api/v1/policy/standard-suite)...")
    suite_r = client.get("/api/v1/policy/standard-suite")
    assert suite_r.status_code == 200
    suite = suite_r.json()
    assert len(suite) >= 6
    print(f"      [PASS] Retrieved {len(suite)} candidate enterprise mitigation policies.")

    # 5. Stochastic Policy Evaluation & Pareto Frontier
    print("[5/10] Testing Stochastic Policy Evaluation (POST /api/v1/policy/evaluate)...")
    pol_r = client.post(
        "/api/v1/policy/evaluate",
        json={
            "num_stochastic_draws": 15,
            "random_seed": 42,
        },
    )
    assert pol_r.status_code == 200, f"Policy eval failed: {pol_r.text}"
    p_data = pol_r.json()
    assert len(p_data["evaluated_policies"]) >= 6
    assert len(p_data["pareto_frontier"]) >= 4
    assert p_data["recommended_policy_id"] is not None
    print(f"      [PASS] Policy evaluation ranked {len(p_data['evaluated_policies'])} policies. "
          f"Recommended: {p_data['recommended_policy_name']}")

    # 6. Risk-Hedged Supplier Dual-Sourcing Optimizer
    print("[6/10] Testing Supplier Dual-Sourcing Optimizer (POST /api/v1/policy/sourcing)...")
    src_r = client.post(
        "/api/v1/policy/sourcing",
        json={
            "annual_demand_units": 150000,
            "shenzhen_disruption_probability": 0.25,
            "saigon_disruption_probability": 0.08,
        },
    )
    assert src_r.status_code == 200, f"Sourcing optimization failed: {src_r.text}"
    src_data = src_r.json()
    assert 0.0 < src_data["optimal_shenzhen_share"] < 1.0
    assert 0.0 < src_data["optimal_saigon_share"] < 1.0
    assert src_data["net_portfolio_savings"] > 0
    print(f"      [PASS] Dual-sourcing split: {int(src_data['optimal_shenzhen_share']*100)}% Shenzhen / "
          f"{int(src_data['optimal_saigon_share']*100)}% Saigon. Avoided Losses: ${src_data['net_portfolio_savings']:,.2f}")

    # 7. Enterprise CSV Upload & Preview
    print("[7/10] Testing Enterprise Data Upload Preview (POST /api/v1/ingestion/preview)...")
    test_csv_content = (
        b"item_code,warehouse_location,on_hand_stock,safety_threshold\n"
        b"APEX-JKT-BLA-XS,reno,850,250\n"
        b"APEX-JKT-BLA-S,allentown,1200,350\n"
        b"APEX-JKT-BLA-M,dallas,650,200\n"
    )
    prev_r = client.post(
        "/api/v1/ingestion/preview",
        files={"file": ("inventory_batch_import.csv", test_csv_content, "text/csv")},
        data={"target_entity": "INVENTORY_SNAPSHOT"},
    )
    assert prev_r.status_code == 200, f"Upload preview failed: {prev_r.text}"
    prev_data = prev_r.json()
    assert prev_data["total_rows"] == 3
    assert prev_data["can_commit"] is True
    print(f"      [PASS] Parsed {prev_data['total_rows']} rows. Mappings: {prev_data['suggested_mapping']}")

    # 8. Transactional Ingestion Commit
    print("[8/10] Testing Transactional Commit (POST /api/v1/ingestion/commit)...")
    commit_r = client.post(
        "/api/v1/ingestion/commit",
        json={
            "file_id": prev_data["file_id"],
            "target_entity": "INVENTORY_SNAPSHOT",
            "column_mapping": prev_data["suggested_mapping"],
            "deduplication_strategy": "REPLACE_EXISTING",
            "impute_missing": True,
        },
    )
    assert commit_r.status_code == 200, f"Commit failed: {commit_r.text}"
    c_data = commit_r.json()
    assert c_data["status"] == "COMMITTED"
    assert c_data["rollback_token"].startswith("RB-")
    print(f"      [PASS] Ingested {c_data['rows_processed']} rows with rollback token {c_data['rollback_token']}.")

    # 9. Transactional Rollback
    print("[9/10] Testing Transactional Rollback (POST /api/v1/ingestion/rollback)...")
    rb_r = client.post(
        "/api/v1/ingestion/rollback",
        json={"rollback_token": c_data["rollback_token"]},
    )
    assert rb_r.status_code == 200, f"Rollback failed: {rb_r.text}"
    rb_data = rb_r.json()
    assert rb_data["status"] == "ROLLED_BACK"
    print(f"      [PASS] Rollback executed cleanly: {rb_data['message']}")

    # 10. Data Quality Monitor & Next.js Build Artifact
    print("[10/10] Auditing Data Quality Monitor & Next.js Build Artifacts...")
    dq_r = client.get("/api/v1/ingestion/quality")
    assert dq_r.status_code == 200
    dq_data = dq_r.json()
    assert dq_data["overall_health_score"] >= 90.0
    assert dq_data["overall_grade"] in ["A+", "A"]

    build_id_path = os.path.join(str(PROJECT_ROOT), "frontend", ".next", "BUILD_ID")
    assert os.path.exists(build_id_path), "Next.js BUILD_ID not found."
    with open(build_id_path, "r", encoding="utf-8") as f:
        b_id = f.read().strip()
    print(f"      [PASS] Data Quality Score: {dq_data['overall_health_score']}% ({dq_data['overall_grade']}). "
          f"Next.js Build ID: {b_id}")

    print("\n" + "=" * 80)
    print("ALL 10 PHASE 3 INTEGRATION CHECKPOINTS PASSED WITH 100% SUCCESS!")
    print("=" * 80)


if __name__ == "__main__":
    test_phase3_integration()
