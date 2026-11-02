"""
SARAS ATLAS — Comprehensive Performance & Latency Benchmark Suite
Measures database query latency, API endpoint latencies (P50/P95/P99),
multi-scenario batch throughput, and process memory consumption.
"""

import os
import sys
import time
import statistics
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from src.api.main import app
from src.database.session import get_db_session
from sqlalchemy import text

client = TestClient(app)


def audit_memory_and_process():
    print("\n--- 1. Process Memory & Host Environment ---")
    health = client.get("/api/v1/health").json()
    mem_info = health.get("memory", {})
    rss_mb = mem_info.get("process_working_set_mb", 0.0)
    peak_mb = mem_info.get("process_peak_working_set_mb", 0.0)
    total_ram_gb = mem_info.get("system_total_phys_gb", 8.0)
    available_ram_gb = mem_info.get("system_avail_phys_gb", 1.5)

    print(f"  Python Process Working Set RSS: {rss_mb:.2f} MB (Peak: {peak_mb:.2f} MB)")
    print(f"  Host Total Physical RAM: {total_ram_gb:.2f} GB | Available: {available_ram_gb:.2f} GB")
    assert rss_mb < 350.0, f"Memory ceiling exceeded: {rss_mb:.2f} MB"
    return {"rss_mb": rss_mb, "peak_mb": peak_mb, "total_ram_gb": total_ram_gb, "available_ram_gb": available_ram_gb}


def audit_database_performance():
    print("\n--- 2. SQLite Database Latency & Throughput ---")
    latencies = []
    with get_db_session() as session:
        # Measure 100 queries
        for _ in range(100):
            t0 = time.perf_counter()
            session.execute(text("SELECT count(*) FROM inventory_snapshots;")).fetchall()
            latencies.append((time.perf_counter() - t0) * 1000)

    p50 = statistics.median(latencies)
    p95 = statistics.quantiles(latencies, n=20)[18] if len(latencies) >= 20 else max(latencies)
    p99 = statistics.quantiles(latencies, n=100)[98] if len(latencies) >= 100 else max(latencies)
    print(f"  SQLite 100 Query Latency: P50={p50:.3f} ms | P95={p95:.3f} ms | P99={p99:.3f} ms")
    assert p50 < 5.0, f"Database latency too high: {p50} ms"
    return {"p50_ms": p50, "p95_ms": p95, "p99_ms": p99}


def audit_api_endpoint_latencies():
    print("\n--- 3. API Endpoint Latency Benchmarks (P50/P95/P99) ---")
    endpoints = [
        ("GET /api/v1/health", lambda: client.get("/api/v1/health")),
        ("GET /api/v1/twin/topology", lambda: client.get("/api/v1/twin/topology")),
        ("GET /api/v1/risks/active", lambda: client.get("/api/v1/risks/active")),
        (
            "POST /api/v1/scenarios/simulate",
            lambda: client.post(
                "/api/v1/scenarios/simulate",
                json={
                    "scenario_name": "Perf Bench",
                    "horizon_days": 90,
                    "shocks": {
                        "supplier_delays": [{"po_number": "PO-9012", "delay_days": 21}],
                        "freight_surcharges": [{"lane_id": "lane_east_coast_parcel", "surcharge_percentage": 0.28}],
                        "demand_elasticities": [{"sku_code": "APEX-JKT", "demand_multiplier": 1.45, "duration_days": 30}],
                    },
                    "mitigations": {"emergency_air_freight_units": 1500},
                },
            ),
        ),
        (
            "POST /api/v1/optimization/solve",
            lambda: client.post(
                "/api/v1/optimization/solve",
                json={"capital_budget_ceiling": 40000.0, "min_service_fill_rate": 0.95, "target_sku": "APEX-JKT"},
            ),
        ),
        ("GET /api/v1/forecasting/evaluate", lambda: client.get("/api/v1/forecasting/evaluate")),
        ("GET /api/v1/rca/trace", lambda: client.get("/api/v1/rca/trace")),
    ]

    benchmark_summary = {}
    for name, req_fn in endpoints:
        lats = []
        # Warmup
        req_fn()
        # 20 samples
        for _ in range(20):
            t0 = time.perf_counter()
            r = req_fn()
            assert r.status_code == 200
            lats.append((time.perf_counter() - t0) * 1000)

        p50 = statistics.median(lats)
        p95 = statistics.quantiles(lats, n=20)[18] if len(lats) >= 20 else max(lats)
        p99 = max(lats)
        benchmark_summary[name] = {"p50": p50, "p95": p95, "p99": p99}
        print(f"  {name:<36} P50: {p50:6.2f} ms | P95: {p95:6.2f} ms | P99: {p99:6.2f} ms")

    return benchmark_summary


def audit_batch_performance():
    print("\n--- 4. Batch Scenario Execution Benchmarks (10, 50, 100 Scenarios) ---")
    batch_results = {}
    for count in [10, 50, 100]:
        scenarios = client.get(f"/api/v1/batch/generate-benchmark?count={count}").json()
        t0 = time.perf_counter()
        resp = client.post(
            "/api/v1/batch/run",
            json={
                "batch_name": f"Perf Batch {count}",
                "scenarios": scenarios,
                "parallel": True,
                "max_workers": 4,
                "persist_results": False,
                "random_seed": 42,
            },
        )
        assert resp.status_code == 200
        dur_ms = (time.perf_counter() - t0) * 1000
        data = resp.json()
        throughput = count / (dur_ms / 1000)
        batch_results[count] = {"duration_ms": dur_ms, "throughput_scn_per_sec": throughput}
        print(f"  Batch {count:3d} Scenarios: {dur_ms:6.1f} ms total ({throughput:6.1f} scenarios/sec)")

    return batch_results


def run_full_performance_audit():
    print("=" * 80)
    print("SARAS ATLAS — COMPREHENSIVE PERFORMANCE & LATENCY BENCHMARK AUDIT")
    print("=" * 80)
    t_start = time.time()

    mem = audit_memory_and_process()
    db = audit_database_performance()
    api = audit_api_endpoint_latencies()
    batch = audit_batch_performance()

    elapsed = time.time() - t_start
    print("\n" + "=" * 80)
    print(f"ALL PERFORMANCE BENCHMARKS COMPLETED IN {elapsed:.2f} SECONDS!")
    print("=" * 80)
    return {"memory": mem, "database": db, "api": api, "batch": batch}


if __name__ == "__main__":
    results = run_full_performance_audit()
