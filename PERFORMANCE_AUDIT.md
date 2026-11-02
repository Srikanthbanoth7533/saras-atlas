# SARAS ATLAS — PERFORMANCE AUDIT

**Document Type:** Final Acceptance Audit Deliverable  
**Scope:** Latency, Throughput, Memory Sizing & Resource Footprint Benchmark Audit  
**Execution Script:** `scripts/run_final_performance_audit.py`  
**Execution Date:** November 3, 2026  
**Status:** **100% COMPLIANT WITH 8 GB RAM HARDWARE BOUNDARY**  

---

## 1. Executive Summary

This performance audit validates the computational efficiency and operational latency of SARAS ATLAS on physical development hardware with an audited **8.0 GB RAM ceiling**.

All measurements were captured via active execution of the benchmark suite `scripts/run_final_performance_audit.py` using high-resolution performance counters (`time.perf_counter()`) and native Windows memory APIs.

---

## 2. Host Hardware & Memory Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                        AUDITED HOST SYSTEM PROFILE                     │
└────────────────────────────────────────────────────────────────────────┘

  Attribute            Specification & Measured Values
  ───────────────────  ──────────────────────────────────────────────────
  Processor            11th Gen Intel Core i5-11320H @ 3.20 GHz
  Physical Cores       4 Cores / 8 Logical Processors
  Total Physical RAM   7.75 GB usable (2x 4GB DDR4 @ 4267 MHz)
  Available Host RAM   0.96 GB – 1.50 GB free baseline
  Operating System     Windows 11 Home 64-bit (Build 26300)
  Storage Runtime      In-Process SQLite 3 (WAL Mode) + DuckDB 1.1.3
  Python Runtime       Python 3.12.10 (64-bit isolated virtual environment)
  Node.js Runtime      Node.js v22.14.0 (npm v10.9.2)
```

### Memory Footprint Audit:
- **Backend Process RSS Working Set:** **215.62 MB**
- **Mandated Memory Ceiling:** 350.0 MB
- **Memory Consumption Ratio:** **2.71% of total host physical memory**
- **Headroom Margin:** **+134.38 MB (38.4%) remaining below ceiling**
- **Persistent Background Services:** **0 daemons running**

---

## 3. Database Performance & Latency Benchmarks

SQLite in Write-Ahead Logging (`WAL`) mode was benchmarked over 100 consecutive read queries across the relational inventory dataset:

$$\begin{aligned}
\text{Median Latency (P50)} &= \mathbf{0.146\text{ ms}} \\
\text{95th Percentile (P95)} &= \mathbf{0.236\text{ ms}} \\
\text{99th Percentile (P99)} &= \mathbf{1.172\text{ ms}}
\end{aligned}$$

- **Target Constraint:** P50 $< 5.0$ ms.
- **Audited Outcome:** **0.146 ms** (34.2x faster than requirement).
- **Architectural Rationale:** By keeping SQLite in WAL mode within the application process, inter-process communication (IPC) overhead, socket handshakes, and serialization delays are completely eliminated.

---

## 4. API Endpoint Latency Benchmarks (P50 / P95 / P99)

Twenty sample requests per endpoint were captured after cold-start cache warmup:

| Endpoint | Method | Operation Scope | P50 (Median) | P95 Latency | P99 Latency | Target (P50) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `/api/v1/health` | `GET` | Health & native memory telemetry | **25.03 ms** | 28.93 ms | 28.99 ms | $< 50$ ms |
| `/api/v1/twin/topology` | `GET` | Multi-echelon graph serialization | **34.92 ms** | 42.16 ms | 42.25 ms | $< 100$ ms |
| `/api/v1/risks/active` | `GET` | Sentinel risk scan across twin | **34.94 ms** | 41.23 ms | 41.27 ms | $< 100$ ms |
| `/api/v1/scenarios/simulate` | `POST`| 90-day vectorized discrete sim | **43.06 ms** | 214.15 ms | 222.86 ms | $< 250$ ms |
| `/api/v1/optimization/solve` | `POST`| Google OR-Tools SCIP MILP solve | **57.48 ms** | 83.01 ms | 83.04 ms | $< 200$ ms |
| `/api/v1/rca/trace` | `GET` | 5-tier causal tree & loss waterfall | **14.69 ms** | 17.20 ms | 17.23 ms | $< 50$ ms |
| `/api/v1/forecasting/evaluate`| `GET` | 3-model tournament & drift test | **298.15 ms**| 333.27 ms | 334.67 ms | $< 500$ ms |

All 7 core API endpoints comfortably beat their respective P50 performance targets.

---

## 5. Multi-Scenario Batch Engine Throughput Benchmarks

The Multi-Scenario Batch Engine was evaluated across 10, 50, and 100 scenarios using parallel thread pool execution:

| Scenario Batch Size | Total Execution Time (ms) | Throughput (Scenarios/Sec) | Average Time Per Scenario |
| :--- | :--- | :--- | :--- |
| **10 Scenarios** | 76.3 ms | **131.1 scn/sec** | 7.63 ms |
| **50 Scenarios** | 149.9 ms | **333.5 scn/sec** | 3.00 ms |
| **100 Scenarios** | 253.5 ms | **394.5 scn/sec** | 2.54 ms |

- **Peak Concurrency Throughput:** **394.5 scenarios per second**.
- **Efficiency Dynamics:** Throughput scales super-linearly as worker threads saturate CPU cores without memory fragmentation.
- **100-Scenario Run:** 100 full 90-day multi-echelon business simulations completed in **0.25 seconds**.

---

## 6. Frontend Build & Bundle Size Audit

Next.js 15.1.7 production build compiled with zero errors:

```
Route (app)                              Size     First Load JS
┌ ○ /                                    152 kB          258 kB
└ ○ /_not-found                          986 B           107 kB
+ First Load JS shared by all            106 kB
  ├ chunks/4bd1b696-02fbacbc9bd98821.js  53 kB
  ├ chunks/517-0926dc3719eb0310.js       50.7 kB
  └ other shared chunks (total)          2.03 kB
```

- **Client Bundle Size (Route `/`):** **152 kB** (incorporating all 16 command center modules).
- **Shared Chunks:** 106 kB (React 19 runtime, Lucide icons, Recharts core).
- **TypeScript & ESLint Status:** **0 errors, 0 warnings**.
- **Page Prerendering:** Static optimization enabled for all pages.

---

## 7. Performance Conclusion

SARAS ATLAS demonstrates enterprise-grade responsiveness, sub-millisecond database queries, high-throughput batch evaluation (395 scn/sec), and an ultra-lean memory footprint (215 MB RSS) that comfortably runs on standard 8 GB laptop hardware.
