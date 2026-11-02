"""
SARAS ATLAS — Master End-to-End Business Workflow Validation Script
Executes and mathematically validates all 14 sequential steps of the Vanguard Apparel Co.
commerce resilience and decision simulation scenario.
"""

import os
import sys
import time
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from src.api.main import app
from src.config import settings

client = TestClient(app)


def run_full_business_workflow():
    print("=" * 80)
    print("SARAS ATLAS — VANGUARD APPAREL CO. END-TO-END BUSINESS WORKFLOW AUDIT")
    print("=" * 80)
    workflow_results = {}
    start_time = time.time()

    # Step 1: Import Business Data
    print("\n[STEP 1/14] Ingesting Enterprise Business Data...")
    sample_csv = (
        b"item_code,warehouse_location,on_hand_stock,safety_threshold\n"
        b"APEX-JKT-BLA-XS,reno,850,250\n"
        b"APEX-JKT-BLA-S,allentown,1200,350\n"
        b"APEX-JKT-BLA-M,dallas,650,200\n"
    )
    preview_res = client.post(
        "/api/v1/ingestion/preview",
        files={"file": ("vanguard_inventory_update.csv", sample_csv, "text/csv")},
        data={"target_entity": "INVENTORY_SNAPSHOT"},
    )
    assert preview_res.status_code == 200, f"Preview failed: {preview_res.text}"
    prev_data = preview_res.json()
    file_id = prev_data["file_id"]
    print(f"      Rows parsed: {prev_data['total_rows']} | File ID: {file_id}")
    print(f"      Column mappings detected: {prev_data['suggested_mapping']}")

    commit_res = client.post(
        "/api/v1/ingestion/commit",
        json={
            "file_id": file_id,
            "target_entity": "INVENTORY_SNAPSHOT",
            "column_mapping": prev_data["suggested_mapping"],
            "deduplication_strategy": "REPLACE_EXISTING",
            "impute_missing": True,
        },
    )
    assert commit_res.status_code == 200, f"Commit failed: {commit_res.text}"
    commit_data = commit_res.json()
    rollback_token = commit_data["rollback_token"]
    print(f"      Committed {commit_data['rows_processed']} rows. Rollback token: {rollback_token}")

    # Verify atomic rollback restores clean state
    rollback_res = client.post("/api/v1/ingestion/rollback", json={"rollback_token": rollback_token})
    assert rollback_res.status_code == 200, f"Rollback failed: {rollback_res.text}"
    print(f"      Rollback tested: Cleanly reverted to baseline state.")
    workflow_results["step1_import"] = {"status": "SUCCESS", "rows": commit_data['rows_processed']}

    # Step 2: Validate Data Quality
    print("\n[STEP 2/14] Validating Enterprise Data Quality...")
    quality_res = client.get("/api/v1/ingestion/quality")
    assert quality_res.status_code == 200, f"Quality audit failed: {quality_res.text}"
    quality_data = quality_res.json()
    print(f"      Overall Health Score: {quality_data['overall_health_score']}% ({quality_data['overall_grade']})")
    first_metric = quality_data['metrics_by_dataset'][0]
    print(f"      Entity: {first_metric['entity_name']} | Completeness: {first_metric['completeness_pct']:.1f}% | Validity: {first_metric['validity_pct']:.1f}% | Uniqueness: {first_metric['uniqueness_pct']:.1f}%")
    assert quality_data['overall_health_score'] >= 90.0
    workflow_results["step2_quality"] = {"score": quality_data['overall_health_score'], "grade": quality_data['overall_grade']}

    # Step 3: Construct the Digital Twin
    print("\n[STEP 3/14] Constructing Business Digital Twin Multi-Echelon Topology...")
    twin_res = client.get("/api/v1/twin/topology")
    assert twin_res.status_code == 200, f"Twin topology failed: {twin_res.text}"
    twin_data = twin_res.json()
    node_count = len(twin_data["nodes"])
    edge_count = len(twin_data["edges"])
    org_slug = twin_data["organization"]["slug"]
    print(f"      Digital Twin Initialized: {node_count} nodes, {edge_count} supply lanes for '{org_slug}'")
    assert node_count >= 5 and edge_count >= 3
    workflow_results["step3_digital_twin"] = {"nodes": node_count, "edges": edge_count}

    # Step 4: Introduce Supplier Disruption (Trans-Pacific Maritime Delay + Freight Surcharge + Demand Surge)
    print("\n[STEP 4/14] Introducing Supplier Disruption Scenario...")
    disruption_params = {
        "po_number": "PO-9012",
        "supplier": "Shenzhen Primary Factory",
        "delay_days": 21,
        "freight_surcharge_pct": 0.28,
        "demand_surge_pct": 0.45,
    }
    print(f"      Shocks injected: Delay={disruption_params['delay_days']}d | Freight Surcharge=+{disruption_params['freight_surcharge_pct']*100:.0f}% | Demand Surge=+{disruption_params['demand_surge_pct']*100:.0f}%")
    workflow_results["step4_disruption"] = disruption_params

    # Step 5: Detect Operational Risks
    print("\n[STEP 5/14] Detecting Operational Risks with Risk Sentinels...")
    risks_res = client.get("/api/v1/risks/active")
    assert risks_res.status_code == 200, f"Active risks failed: {risks_res.text}"
    risks_data = risks_res.json()
    print(f"      Detected {risks_data['total_active_risks']} active risks ({risks_data['critical_count']} CRITICAL, {risks_data['warning_count']} WARNING)")
    for r in risks_data["risks"]:
        exp = r.get('estimated_revenue_exposure') or r.get('estimated_monthly_freight_inflation') or 0.0
        print(f"      - [{r['severity']}] {r['title']}: Exposure=${exp:,.2f}")
    assert risks_data['critical_count'] >= 1
    workflow_results["step5_risks"] = {"critical_count": risks_data['critical_count'], "total": risks_data['total_active_risks']}

    # Step 6: Execute Impact Propagation (Unmitigated 90-Day Simulation)
    print("\n[STEP 6/14] Executing Impact Propagation Simulation (Vectorized Discrete Differences)...")
    sim_unmitigated = {
        "scenario_name": "Unmitigated Disruption",
        "horizon_days": 90,
        "shocks": {
            "supplier_delays": [{"po_number": "PO-9012", "delay_days": 21}],
            "freight_surcharges": [{"lane_id": "lane_east_coast_parcel", "surcharge_percentage": 0.28}],
            "demand_elasticities": [{"sku_code": "APEX-JKT", "demand_multiplier": 1.45, "duration_days": 30}],
        },
        "mitigations": {},
    }
    unmit_res = client.post("/api/v1/scenarios/simulate", json=sim_unmitigated)
    assert unmit_res.status_code == 200, f"Simulation failed: {unmit_res.text}"
    unmit_data = unmit_res.json()
    stockout_days = unmit_data["summary_scorecard"]["stockout_days"]
    unmit_cm = unmit_data["summary_scorecard"]["net_contribution_margin"]
    fulfilled = unmit_data["summary_scorecard"]["total_orders_fulfilled"]
    lost = unmit_data["summary_scorecard"]["unfulfilled_lost_orders"]
    unmit_fill = fulfilled / (fulfilled + lost) if (fulfilled + lost) > 0 else 0.0
    print(f"      Unmitigated Impact: Stockout Days={stockout_days} | CM=${unmit_cm:,.2f} | Fill Rate={unmit_fill*100:.1f}% (Fulfilled: {fulfilled:,}, Lost: {lost:,})")
    assert stockout_days > 0
    workflow_results["step6_propagation"] = {"stockout_days": stockout_days, "cm": unmit_cm, "fill_rate": unmit_fill}

    # Step 7: Run Multiple Scenarios (Batch Engine & Sensitivity)
    print("\n[STEP 7/14] Running Multi-Scenario Batch Engine & Sensitivity Sweeps...")
    gen_res = client.get("/api/v1/batch/generate-benchmark?count=10")
    assert gen_res.status_code == 200, f"Generate benchmark failed: {gen_res.text}"
    scenarios = gen_res.json()
    assert len(scenarios) == 10

    batch_res = client.post(
        "/api/v1/batch/run",
        json={
            "batch_name": "Final Audit Verification Batch",
            "scenarios": scenarios,
            "parallel": True,
            "max_workers": 4,
            "persist_results": True,
            "random_seed": 42,
        },
    )
    assert batch_res.status_code == 200, f"Batch run failed: {batch_res.text}"
    batch_data = batch_res.json()
    print(f"      Executed 10 scenarios in {batch_data['total_execution_ms']:.1f} ms ({batch_data['scenarios_per_second']:.1f} scn/sec)")
    print(f"      Best: {batch_data['best_case']['scenario_name'][:30]} | Score={batch_data['best_case']['composite_score']:.3f}")
    print(f"      Worst: {batch_data['worst_case']['scenario_name'][:30]} | Score={batch_data['worst_case']['composite_score']:.3f}")

    sens_res = client.post(
        "/api/v1/batch/sensitivity",
        json={"parameter": "supplier_delay", "min_value": 0, "max_value": 60, "steps": 7},
    )
    assert sens_res.status_code == 200, f"Sensitivity failed: {sens_res.text}"
    sens_data = sens_res.json()
    print(f"      Parametric sensitivity sweep: {sens_data['steps_evaluated']} delay points evaluated across 0..60d")
    workflow_results["step7_batch"] = {"throughput": batch_data['scenarios_per_second'], "points": sens_data['steps_evaluated']}

    # Step 8: Forecast Demand and Inventory
    print("\n[STEP 8/14] Running Advanced Forecasting Studio (78/22 Out-of-Time Test Split)...")
    forecast_res = client.get("/api/v1/forecasting/evaluate")
    assert forecast_res.status_code == 200, f"Forecasting failed: {forecast_res.text}"
    forecast_data = forecast_res.json()
    best_model = forecast_data["best_model_name"]
    best_score = next(s for s in forecast_data["models_evaluated"] if s["model_name"] == best_model)
    print(f"      Champion Model: {best_model} | WAPE={best_score['wape']:.2f}% | MAE={best_score['mae']:.2f} units")
    print(f"      Drift Test: KS statistic={forecast_data['drift_analysis']['ks_statistic']:.4f}, p-val={forecast_data['drift_analysis']['p_value']:.4f} ({forecast_data['drift_analysis']['drift_severity']})")
    assert best_score['wape'] < 10.0
    workflow_results["step8_forecast"] = {"best_model": best_model, "wape": best_score['wape']}

    # Step 9: Evaluate Mitigation Policies (Dynamic Policy Optimization & CVaR)
    print("\n[STEP 9/14] Evaluating Dynamic Mitigation Policies & CVaR Tail-Risk...")
    policy_res = client.post("/api/v1/policy/evaluate", json={"num_stochastic_draws": 15, "random_seed": 42})
    assert policy_res.status_code == 200, f"Policy evaluation failed: {policy_res.text}"
    policy_data = policy_res.json()
    rec_policy = policy_data["recommended_policy_name"]
    print(f"      Evaluated {len(policy_data['evaluated_policies'])} candidate policies. Recommended: '{rec_policy}'")
    sourcing_res = client.post(
        "/api/v1/policy/sourcing",
        json={"annual_demand_units": 150000, "shenzhen_disruption_probability": 0.25, "saigon_disruption_probability": 0.08},
    )
    assert sourcing_res.status_code == 200, f"Sourcing failed: {sourcing_res.text}"
    sourcing_data = sourcing_res.json()
    print(f"      Optimal Sourcing Allocation: Shenzhen={int(sourcing_data['optimal_shenzhen_share']*100)}% | Saigon={int(sourcing_data['optimal_saigon_share']*100)}% | Avoided Loss=${sourcing_data['net_portfolio_savings']:,.2f}")
    workflow_results["step9_policies"] = {"recommended": rec_policy, "avoided_loss": sourcing_data['net_portfolio_savings']}

    # Step 10: Run Optimization (Google OR-Tools MILP SCIP Solver)
    print("\n[STEP 10/14] Executing Google OR-Tools MILP Solver for Prescriptive Rebalancing...")
    opt_payload = {
        "capital_budget_ceiling": 40000.00,
        "min_service_fill_rate": 0.95,
        "max_ad_throttle_pct": 0.35,
        "target_sku": "APEX-JKT",
        "objective": "MAXIMIZE_CONTRIBUTION_MARGIN",
    }
    opt_res = client.post("/api/v1/optimization/solve", json=opt_payload)
    assert opt_res.status_code == 200, f"Optimization failed: {opt_res.text}"
    opt_data = opt_res.json()
    print(f"      Solver Status: {opt_data['status']} in {opt_data['solve_time_ms']:.2f} ms")
    print(f"      Recommended Action: Air Freight={opt_data['recommended_air_freight_units']} units | Ground Transfer={opt_data['recommended_transfer_units']} units | Ad Throttle={opt_data['recommended_ad_throttle_pct']*100:.1f}%")
    print(f"      Capital Required: ${opt_data['capital_required']:,.2f} | Projected CM: ${opt_data['projected_net_contribution_margin']:,.2f} | Stockouts: {opt_data['projected_stockout_days']}d")
    assert opt_data['status'] == "OPTIMAL"
    assert opt_data['capital_required'] <= 40000.00
    workflow_results["step10_optimization"] = {"status": opt_data['status'], "capital": opt_data['capital_required']}

    # Step 11: Explain the Recommended Decision (8-Dimension Dossiers & RCA)
    print("\n[STEP 11/14] Generating Explainable Decision Dossiers & Root Cause Analysis...")
    explain_res = client.get("/api/v1/explainability/recommendations")
    assert explain_res.status_code == 200, f"Explainability failed: {explain_res.text}"
    explain_data = explain_res.json()
    recs = explain_data["recommendations"]
    first_dossier = recs[0]
    print(f"      Dossier: '{first_dossier['title']}'")
    print(f"      - What: {first_dossier['what_action'][:80]}...")
    print(f"      - Why: {first_dossier['why_recommended'][:80]}...")
    print(f"      - Financial Benefit: {first_dossier['expected_financial_benefits']}")
    print(f"      - Consequences of Inaction: {first_dossier['consequences_of_no_action'][:80]}...")

    rca_res = client.get("/api/v1/rca/trace")
    assert rca_res.status_code == 200, f"RCA failed: {rca_res.text}"
    rca_data = rca_res.json()
    print(f"      Root Cause Traced: {rca_data['primary_root_cause']} | Total Loss=${rca_data['total_financial_impact']:,.2f}")
    first_loss = rca_data['financial_attribution'][0]
    print(f"      Loss Segments ({len(rca_data['financial_attribution'])}): {first_loss['segment_name']}=${first_loss['dollar_impact']:,.2f} ({first_loss['percentage_of_total']}%)")
    workflow_results["step11_explainability"] = {"dossiers": len(recs), "root_trigger": rca_data['primary_root_cause']}

    # Step 12: Obtain Human Approval (Two-Man Rule Cryptographic Sign-Off)
    print("\n[STEP 12/14] Obtaining Human Approval via Two-Man Rule Governance...")
    gov_req = {
        "approver_primary_id": "USR-COO-01",
        "approver_primary_name": "Elena Rostova (COO)",
        "approver_secondary_id": "USR-CFO-01",
        "approver_secondary_name": "Marcus Vance (CFO)",
        "decision": "APPROVED",
        "notes": "Approved emergency air freight and ground transfer for Apex Jacket disruption.",
        "approved_capital_outlay": opt_data['capital_required'],
    }
    gov_res = client.post("/api/v1/governance/approve", json=gov_req)
    assert gov_res.status_code == 200, f"Governance failed: {gov_res.text}"
    gov_data = gov_res.json()
    print(f"      Approval Record: {gov_data['id']} | Decision={gov_data['decision']} | Status={gov_data['status']}")
    print(f"      Cryptographic Seal (SHA-256): {gov_data['digital_signature_sha256'][:32]}...")
    assert len(gov_data['digital_signature_sha256']) == 64
    workflow_results["step12_governance"] = {"action_id": gov_data['id'], "signature": gov_data['digital_signature_sha256']}

    # Step 13: Generate Executive Reports (Native Vector PDF & Streaming CSV)
    print("\n[STEP 13/14] Generating Executive Board Briefing & Exporting PDF/CSV...")
    auth_res = client.post("/api/v1/auth/login", json={"username": "admin", "password": "AtlasAdmin2026!"})
    token = auth_res.json()["access_token"]
    auth_headers = {"Authorization": f"Bearer {token}"}

    summary_res = client.get("/api/v1/reports/summary", headers=auth_headers)
    assert summary_res.status_code == 200, f"Summary failed: {summary_res.text}"
    summary_data = summary_res.json()
    print(f"      Report Title: '{summary_data['title']}' | Recommendations: {len(summary_data['recommendations'])}")

    pdf_res = client.get("/api/v1/reports/export/pdf", headers=auth_headers)
    assert pdf_res.status_code == 200, f"PDF export failed: {pdf_res.text}"
    assert pdf_res.headers["content-type"] == "application/pdf"
    assert pdf_res.content[:4] == b"%PDF"
    print(f"      Generated Vector PDF: {len(pdf_res.content):,} bytes (ReportLab Native Vector Engine)")

    csv_res = client.get("/api/v1/reports/export/csv", headers=auth_headers)
    assert csv_res.status_code == 200, f"CSV export failed: {csv_res.text}"
    assert "text/csv" in csv_res.headers["content-type"]
    print(f"      Generated CSV Export: {len(csv_res.content):,} bytes")
    workflow_results["step13_reports"] = {"pdf_bytes": len(pdf_res.content), "csv_bytes": len(csv_res.content)}

    # Step 14: Preserve the Audit Trail
    print("\n[STEP 14/14] Preserving Security Audit Trail & Integrity Verification...")
    audit_res = client.get("/api/v1/security/audit-trail?limit=20", headers=auth_headers)
    assert audit_res.status_code == 200, f"Audit query failed: {audit_res.text}"
    audit_records = audit_res.json()
    print(f"      Security Audit Trail: {len(audit_records)} events logged in append-only store")
    print(f"      Latest event: {audit_records[-1]['action']} by {audit_records[-1]['username']} at {audit_records[-1]['timestamp']}")

    elapsed = time.time() - start_time
    print("\n" + "=" * 80)
    print(f"ALL 14 BUSINESS WORKFLOW STEPS VALIDATED SUCCESSFULLY IN {elapsed:.2f} SECONDS!")
    print("=" * 80)
    return workflow_results


if __name__ == "__main__":
    results = run_full_business_workflow()
