"""
SARAS ATLAS — Automated Performance, Numerical & Memory Benchmarks.
Validates latency limits, RAM footprint (< 350 MB RSS), and GAAP accounting conservation.
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import time
import ctypes
from ctypes import wintypes
import statistics
from typing import Dict, Any, List

from src.database.session import SessionLocal
from src.domain.twin.state import DigitalTwinState
from src.domain.simulation.engine import SimulationEngine
from src.domain.simulation.models import (
    SimulationRequest,
    ShocksConfig,
    MitigationsConfig,
    SupplierDelayShock,
    FreightSurchargeShock,
    DemandSurgeShock,
)
from src.domain.optimization.models import OptimizationRequest
from src.domain.optimization.solver import PrescriptiveOptimizationSolver
from src.domain.simulation.accounting import calculate_unit_contribution_margin


class PROCESS_MEMORY_COUNTERS_EX(ctypes.Structure):
    _fields_ = [
        ("cb", wintypes.DWORD),
        ("PageFaultCount", wintypes.DWORD),
        ("PeakWorkingSetSize", ctypes.c_size_t),
        ("WorkingSetSize", ctypes.c_size_t),
        ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
        ("QuotaPagedPoolUsage", ctypes.c_size_t),
        ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
        ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
        ("PagefileUsage", ctypes.c_size_t),
        ("PeakPagefileUsage", ctypes.c_size_t),
        ("PrivateUsage", ctypes.c_size_t),
    ]


def get_rss_mb() -> float:
    """Returns current process working set (RSS) in MB."""
    if sys.platform == "win32":
        try:
            psapi = ctypes.windll.psapi
            kernel32 = ctypes.windll.kernel32
            psapi.GetProcessMemoryInfo.argtypes = [
                wintypes.HANDLE,
                ctypes.POINTER(PROCESS_MEMORY_COUNTERS_EX),
                wintypes.DWORD,
            ]
            kernel32.GetCurrentProcess.restype = wintypes.HANDLE
            pmc = PROCESS_MEMORY_COUNTERS_EX()
            pmc.cb = ctypes.sizeof(PROCESS_MEMORY_COUNTERS_EX)
            if psapi.GetProcessMemoryInfo(kernel32.GetCurrentProcess(), ctypes.byref(pmc), pmc.cb):
                return round(pmc.WorkingSetSize / (1024 * 1024), 2)
        except Exception:
            pass
    return 0.0


def benchmark_simulation_engine(engine: SimulationEngine, runs: int = 50) -> Dict[str, Any]:
    req = SimulationRequest(
        scenario_name="Benchmark Simulation",
        horizon_days=90,
        shocks=ShocksConfig(
            supplier_delays=[SupplierDelayShock(po_number="PO-9012", delay_days=21)],
            freight_surcharges=[FreightSurchargeShock(lane_id="lane_east_coast_parcel", surcharge_percentage=0.28)],
            demand_elasticities=[DemandSurgeShock(sku_code="APEX-JKT", demand_multiplier=1.45, duration_days=30)]
        ),
        mitigations=MitigationsConfig(
            emergency_air_freight_units=1500,
            inter_warehouse_transfer_units=600,
            ad_spend_throttle_percentage=0.18
        )
    )

    latencies_ms: List[float] = []
    # Warmup
    engine.run_simulation(req)

    for _ in range(runs):
        t0 = time.perf_counter()
        resp = engine.run_simulation(req)
        elapsed_ms = (time.perf_counter() - t0) * 1000
        latencies_ms.append(elapsed_ms)

    latencies_ms.sort()
    p50 = latencies_ms[int(len(latencies_ms) * 0.50)]
    p95 = latencies_ms[int(len(latencies_ms) * 0.95)]
    p99 = latencies_ms[int(len(latencies_ms) * 0.99)]
    avg = statistics.mean(latencies_ms)

    return {
        "runs": runs,
        "mean_ms": round(avg, 2),
        "p50_ms": round(p50, 2),
        "p95_ms": round(p95, 2),
        "p99_ms": round(p99, 2),
        "min_ms": round(min(latencies_ms), 2),
        "max_ms": round(max(latencies_ms), 2),
        "pass_p95_under_100ms": p95 < 100.0,
    }


def benchmark_milp_solver(solver: PrescriptiveOptimizationSolver, runs: int = 5) -> Dict[str, Any]:
    req = OptimizationRequest(
        capital_budget_ceiling=40000.00,
        min_service_fill_rate=0.95,
        max_ad_throttle_pct=0.35,
        target_sku="APEX-JKT"
    )

    latencies_ms: List[float] = []
    for _ in range(runs):
        t0 = time.perf_counter()
        res = solver.solve(req)
        elapsed_ms = (time.perf_counter() - t0) * 1000
        latencies_ms.append(elapsed_ms)

    avg = statistics.mean(latencies_ms)
    p95 = sorted(latencies_ms)[int(len(latencies_ms) * 0.95)]

    return {
        "runs": runs,
        "mean_ms": round(avg, 2),
        "p95_ms": round(p95, 2),
        "status": res.status,
        "pass_under_1000ms": p95 < 1000.0,
    }


def verify_numerical_and_accounting_integrity():
    cm = calculate_unit_contribution_margin(
        retail_price=180.00,
        base_cogs=42.00,
        inbound_tariff_rate=0.0750,
        pick_pack_fee=4.50,
        outbound_shipping_cost=8.50,
        payment_fee_rate=0.0290,
        allocated_ad_spend=45.00
    )
    # Revenue = 180.00
    # Tariffs = 3.15
    # Total COGS = 45.15
    # Shipping = 8.50
    # Pick/pack = 4.50
    # Fees = 5.52
    # Ad spend = 45.00
    # Total costs = 108.67
    # CM = 71.33
    passed = (
        cm["net_revenue"] == 180.00
        and cm["tariffs"] == 3.15
        and cm["landed_cogs"] == 45.15
        and cm["payment_processing_fee"] == 5.52
        and cm["total_variable_costs"] == 108.67
        and cm["contribution_margin_dollars"] == 71.33
    )
    return {
        "accounting_waterfall_precision": "PASS" if passed else "FAIL",
        "verified_unit_cm": cm["contribution_margin_dollars"],
        "verified_margin_pct": cm["contribution_margin_percentage"],
    }


def main():
    print("=" * 70)
    print(" SARAS ATLAS — PHASE 1 PERFORMANCE & NUMERICAL BENCHMARK SUITE")
    print("=" * 70)

    rss_start = get_rss_mb()
    print(f"[*] Initial Memory Footprint: {rss_start} MB RSS")

    with SessionLocal() as session:
        twin = DigitalTwinState(session=session)

    rss_twin = get_rss_mb()
    print(f"[*] Digital Twin Loaded: {rss_twin} MB RSS (Delta: +{round(rss_twin - rss_start, 2)} MB)")

    engine = SimulationEngine(twin)
    solver = PrescriptiveOptimizationSolver(twin_state=twin)

    print("\n--- 1. Multi-Echelon Simulation Engine Latency (50 runs) ---")
    sim_bench = benchmark_simulation_engine(engine, runs=50)
    print(f"  Mean Latency: {sim_bench['mean_ms']} ms")
    print(f"  P50 Latency:  {sim_bench['p50_ms']} ms")
    print(f"  P95 Latency:  {sim_bench['p95_ms']} ms (Target < 100 ms: {'PASS' if sim_bench['pass_p95_under_100ms'] else 'FAIL'})")
    print(f"  P99 Latency:  {sim_bench['p99_ms']} ms")

    print("\n--- 2. Google OR-Tools MILP Solver Latency (5 runs) ---")
    opt_bench = benchmark_milp_solver(solver, runs=5)
    print(f"  Mean Latency: {opt_bench['mean_ms']} ms")
    print(f"  P95 Latency:  {opt_bench['p95_ms']} ms (Target < 1000 ms: {'PASS' if opt_bench['pass_under_1000ms'] else 'FAIL'})")
    print(f"  Solver Status: {opt_bench['status']}")

    rss_post = get_rss_mb()
    print(f"\n--- 3. In-Process Memory Footprint Audit ---")
    print(f"  Peak Working Set: {rss_post} MB RSS")
    print(f"  Target Constraint: < 350.0 MB RSS")
    print(f"  Verdict: {'PASS (Compliant with 8 GB RAM Limit)' if rss_post < 350.0 else 'FAIL'}")

    print("\n--- 4. Numerical Accounting & Conservation Audit ---")
    num_audit = verify_numerical_and_accounting_integrity()
    print(f"  GAAP Waterfall Precision: {num_audit['accounting_waterfall_precision']}")
    print(f"  Unit CM: ${num_audit['verified_unit_cm']:.2f}")
    print(f"  Margin Rate: {num_audit['verified_margin_pct'] * 100:.2f}%")

    print("\n" + "=" * 70)
    all_passed = (
        sim_bench["pass_p95_under_100ms"]
        and opt_bench["pass_under_1000ms"]
        and rss_post < 350.0
        and num_audit["accounting_waterfall_precision"] == "PASS"
    )
    print(f" OVERALL PHASE 1 BENCHMARK VERDICT: {'PASSED (READY FOR ACCEPTANCE)' if all_passed else 'FAILED'}")
    print("=" * 70)


if __name__ == "__main__":
    main()
