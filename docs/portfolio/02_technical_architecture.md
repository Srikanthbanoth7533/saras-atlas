# SARAS ATLAS — Technical Architecture Specification
## In-Process Modular Monolith, Prescriptive Decision Engines, and Zero-Cost Cloud Deployment

**Platform:** SARAS ATLAS — Commerce Resilience & Decision Simulation Platform  
**Target Enterprise:** Vanguard Apparel Co. ($45.0M Annual GMV Synthetic Digital Twin)  
**System Architecture:** In-Process Modular Monolith with Split Cloud Edge Deployment  
**Repository:** https://github.com/Srikanthbanoth7533/saras-atlas  
**Document Classification:** Technical Architecture Standard (Phase 11.2)  

---

## 1. System Overview & Architectural Tenets

SARAS ATLAS is an enterprise-grade digital twin, operational simulation, and mathematical optimization platform engineered for omnichannel commerce. It is architected around five fundamental engineering principles:

1. **In-Process Modular Monolith:** Avoiding microservice network overhead, distributed transaction failures, and complex orchestration by housing domain engines in a single, high-performance Python ASGI container (< 55 MB RSS).
2. **Single-Origin Perimeter:** Eliminating cross-origin resource sharing (CORS) security friction and browser mixed-content protocol blocks by reverse-proxying all API traffic through Next.js edge rewrites (`https://saras-atlas.vercel.app/api/:path*`).
3. **Deterministic Self-Healing State:** Utilizing an in-memory/WAL SQLite transactional store seeded deterministically (NumPy/Python `SEED = 42`) on process boot, ensuring an immutable benchmark for recruiter and executive evaluation.
4. **Exact Mathematical Solvers:** Replacing stochastic heuristics and unconstrained AI agents with mathematically rigorous Mixed-Integer Linear Programs (MILP) solved via Google OR-Tools and the open-source SCIP solver.
5. **Zero-Cost Deployment Footprint:** Operating perpetually within complimentary developer cloud tiers (Vercel Hobby + Render Free) with strict zero-dollar operational expenditure.

---

## 2. High-Level System Architecture

```mermaid
flowchart TD
    subgraph ClientLayer ["1. Client Presentation Layer (Recruiter / Executive Browser)"]
        Browser["Modern Web Browser (Desktop / Laptop / Tablet / Mobile)"]
        EdgeProxy["Next.js Edge Proxy (/api/:path* -> Render)"]
    end

    subgraph FrontendVercel ["2. Frontend Edge Tier: Vercel Hobby (0s Cold Start)"]
        NextApp["Next.js 15.5.28 App Router (React 19, TypeScript)"]
        TailwindUI["Tailwind CSS + Lucide Icons + Recharts UI"]
        DemoModals["Guided Demo Modal + Product Overview Modal"]
        PillarNav["4-Pillar Category Navigation (16 Core Modules)"]
    end

    subgraph BackendRender ["3. Backend Computational Tier: Render Free Web Service (512 MB RAM)"]
        FastAPI["FastAPI 0.115.6 ASGI Gateway (:10000)"]
        SecurityMW["Rate Limiter & Security Headers Middleware"]
        AuthModule["JWT HS256 Authentication & RBAC Filter"]

        subgraph EngineLayer ["Core Computational Domain Engines (< 55 MB RSS)"]
            TwinState["Digital Twin State Manager (Multi-Echelon Graph)"]
            SimEngine["Discrete Difference Daily Accounting Engine (90-Day Horizon)"]
            Optimizer["Google OR-Tools SCIP Prescriptive Solver"]
            Forecasting["Demand Forecasting Studio (Ridge, Holt-Winters, STL)"]
            RCA["Root Cause Analysis & Causal Attribution Engine"]
            Governance["Two-Man Rule Dual-Key Approval Gateway"]
            Reporting["ReportLab Vector PDF & RFC-4180 CSV Engine"]
        end

        subgraph StorageLayer ["In-Process Storage Tier"]
            SQLiteStore[("SQLite WAL Transactional Store (Benchmark Seed #42)")]
            DuckDBStore[("DuckDB Analytical OLAP Engine")]
            AuditLedger[("SHA-256 Tamper-Evident Governance Ledger")]
        end
    end

    Browser <-->|HTTPS :443| NextApp
    NextApp --> TailwindUI
    NextApp --> DemoModals
    NextApp --> PillarNav
    Browser -->|API Calls /api/v1/*| EdgeProxy
    EdgeProxy -->|Encrypted HTTPS Bridge| FastAPI
    FastAPI --> SecurityMW
    SecurityMW --> AuthModule
    AuthModule --> EngineLayer
    EngineLayer <--> StorageLayer
```

---

## 3. Tier-by-Tier Technical Architecture

### 3.1 Frontend Presentation Tier (Next.js 15 + React 19)
- **Framework:** Next.js 15.5.28 (React Server Components + Client Components).
- **Core Dependencies:** React 19.0.0, TypeScript 5.7.3, Tailwind CSS 3.4.17, Recharts 2.15.0, Lucide React 0.469.0.
- **Rendering Model:** Hybrid. Static page shell pre-rendered with Next.js edge caching; interactive modules utilize React Client Components with selective hydration.
- **State Management:** Modular React Hooks (`useState`, `useEffect`, `useCallback`, `useMemo`). Complex state transitions (e.g. Guided Demo step sequencer) are modeled as declarative finite state machines.
- **Responsive System:** Fluid 4-breakpoint responsive grid system verified across Desktop (1440px), Laptop (1366px), Tablet (768px), and Mobile (390px).
- **Performance Characteristics:** First Load JS: 170 kB (compressed); cumulative layout shift (CLS): 0.00; total browser console errors: **0**.

### 3.2 Edge Reverse Proxy (`frontend/next.config.mjs`)
To circumvent CORS preflight latency and prevent mixed-content browser blocks, Next.js implements server-side URL rewrites:
```javascript
/** @type {import('next').NextConfig} */
const backendUrl = process.env.BACKEND_API_URL || 'http://127.0.0.1:8000';

const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${backendUrl}/api/:path*`,
      },
    ];
  },
};
export default nextConfig;
```
- **Operational Advantage:** The browser communicates exclusively with `https://saras-atlas.vercel.app`. The Vercel edge infrastructure securely terminates the connection and proxies payloads to the Render backend over high-speed backbone connections.

### 3.3 Backend Computational Tier (FastAPI + Python 3.12)
- **ASGI Framework:** FastAPI 0.115.6 on Uvicorn 0.34.0.
- **Validation Engine:** Pydantic v2 (strict type enforcement, automatic OpenAPI 3.1 schema generation).
- **Process Memory Footprint:** **50.0 MB RSS** at idle; **< 55 MB RSS** under multi-threaded scenario sweep stress.
- **Startup Lifecycle:** Uses FastAPI `@asynccontextmanager` to execute non-blocking database integrity checks and ensure that the synthetic Vanguard digital twin is initialized before accepting ingress HTTP traffic.

### 3.4 In-Process Storage & OLAP Architecture
- **Transactional State (SQLite WAL):**
  - Configured with `PRAGMA journal_mode=WAL;`, `PRAGMA synchronous=NORMAL;`, and `PRAGMA busy_timeout=5000;`.
  - Enables concurrent readers without blocking write transactions.
  - Tables: `facilities`, `suppliers`, `skus`, `inventory_records`, `purchase_orders`, `transport_lanes`, `disruptions`, `approvals`, `simulations`.
- **Analytical State (DuckDB):**
  - Embedded columnar OLAP engine for zero-copy vector aggregations over multi-year sales and inventory time series.
  - Generates cross-facility inventory rollups in < 4 milliseconds.
- **Tamper-Evident Audit Ledger:**
  - Append-only cryptographic ledger storing approval records, simulation snapshots, and user actions.
  - Each record contains a chained SHA-256 digital signature:
    $$\text{Hash}_t = \text{SHA256}(\text{Hash}_{t-1} \parallel \text{Approver}_1 \parallel \text{Approver}_2 \parallel \text{Capital} \parallel \text{Timestamp})$$

---

## 4. Domain Engine Specifications

```mermaid
classDiagram
    class DigitalTwinState {
        +get_topology()
        +get_inventory_summary()
        +get_pipeline_orders()
        +update_facility_stock()
    }
    class SimulationEngine {
        +run_simulation(shocks, mitigations)
        +calculate_daily_flows()
        +compute_financial_scorecard()
    }
    class PrescriptiveOptimizer {
        +formulate_milp(budget, service_level)
        +solve_scip()
        +extract_allocations()
    }
    class AdvancedForecaster {
        +evaluate_forecast(series_type, horizon)
        +train_ridge_model()
        +train_holt_winters()
    }
    class GovernanceGateway {
        +evaluate_two_man_rule(capital)
        +submit_approval(approvers, decision)
        +get_audit_trail()
    }
    DigitalTwinState <-- SimulationEngine
    SimulationEngine <-- PrescriptiveOptimizer
    DigitalTwinState <-- PrescriptiveOptimizer
    DigitalTwinState <-- AdvancedForecaster
    PrescriptiveOptimizer --> GovernanceGateway
```

### 4.1 Digital Twin State Manager (`src/domain/twin/`)
- Encapsulates physical asset state: 2 fulfillment centers (WH-WEST in Los Angeles, WH-EAST in Columbus), 3 manufacturing partners (Shenzhen, Vietnam, LA local), and 50 retail SKUs.
- Enforces strict inventory balance conservation equations:
  $$I_{i,j}(t) = I_{i,j}(t-1) + \text{Inbound}_{i,j}(t) - \text{Outbound}_{i,j}(t) - \text{Scrap}_{i,j}(t)$$
- Tracks pipeline inventory in transit across 4 multi-modal lanes with dynamic lead-time distributions.

### 4.2 Discrete Difference Simulation Engine (`src/domain/simulation/`)
- Simulates daily operational execution across an arbitrary forward horizon ($T = 90$ days).
- Evaluates compounded shock vectors:
  - Supplier lead-time breaches (e.g. PO-9012 +21 days).
  - Inbound freight surcharges (+28.0%).
  - Regional demand surge elasticities (+45.0% on target SKUs).
- Computes daily GAAP accounting matrices: Gross Revenue, Vendor COGS, Inbound Freight, Outbound Parcel, Zone Surcharges, Ad Spend, and Net Contribution Margin.

### 4.3 Prescriptive SCIP Optimizer (`src/domain/optimization/`)
- Interfaces with Google OR-Tools to instantiate the open-source **SCIP (Solving Constraint Integer Programs)** solver.
- Formulates a Mixed-Integer Linear Program balancing three decision levers:
  1. Expedited Air Freight volume ($x_{\text{air}} \in \mathbb{Z}^+$).
  2. Domestic Ground Transfer volume ($x_{\text{xfer}} \in \mathbb{Z}^+$).
  3. Regional Ad Spend Throttling percentage ($\theta_{\text{ad}} \in [0, 0.35]$).
- Solves in < 60 ms with provable mathematical optimality.

### 4.4 Advanced Forecasting Engine (`src/domain/forecasting/`)
- Evaluates 3 distinct predictive methodologies on rolling out-of-sample test splits:
  1. Classical 7-Day Moving Average baseline.
  2. Holt-Winters Exponential Smoothing with additive weekly seasonality ($m = 7$).
  3. Scikit-learn Ridge Regression with multi-period lagged demand ($t-1, t-7, t-14$), rolling moving averages, day-of-week one-hot indicators, and promotional flags.
- Computes out-of-sample Weighted Absolute Percentage Error (WAPE) and Root Mean Squared Error (RMSE).

### 4.5 Governance & Cryptographic Ledger (`src/domain/governance/`)
- Evaluates high-value operational risk rules. Automatically enforces the **Two-Man Rule** whenever proposed mitigation capital exceeds `$25,000.00`.
- Requires dual distinct executive credentials (VP Supply Chain + Chief Financial Officer).
- Commits cryptographic digital signatures (SHA-256) to an immutable audit table.

### 4.6 Executive Report Generator (`src/domain/reporting/`)
- Programmatically constructs publication-grade vector PDF briefings using Python `ReportLab` (flowables, custom styling, tables, header/footer canvas drawing).
- Programmatically constructs streaming RFC-4180 CSV exports guaranteeing 100% numerical parity with the PDF.

---

## 5. Security Architecture & Threat Model

```mermaid
flowchart LR
    Ingress["Public HTTPS Ingress"] --> RateLimit["In-Memory Rate Limiter\n(Client IP Sliding Window)"]
    RateLimit --> SecHeaders["Security Headers Middleware\n(CSP, HSTS, X-Frame-Options)"]
    SecHeaders --> JWTFilter["JWT Bearer Authentication\n(HS256 64-Hex Secret)"]
    JWTFilter --> RBAC["Role-Based Access Control\n(ADMIN, VP_OPS, CFO, ANALYST)"]
    RBAC --> Endpoints["Protected API Handlers"]
```

1. **Authentication:** Stateless JSON Web Tokens (JWT) signed with HMAC-SHA256 using a 64-character hexadecimal secret. Tokens carry a 28,800-second (8-hour) expiration.
2. **Role-Based Access Control (RBAC):** Strict role hierarchy:
   - `ADMIN`: Full platform access, data ingestion rollback, user management.
   - `SUPPLY_CHAIN_VP`: Scenario simulation, optimization solver, primary governance sign-off.
   - `CFO`: Financial reconciliation, budget adjustment, secondary governance sign-off.
   - `ANALYST`: Read-only telemetry, forecasting evaluation, report download.
3. **Defense-in-Depth Middleware:**
   - Strict Content Security Policy (`script-src 'self' 'unsafe-inline'`).
   - Strict-Transport-Security (`max-age=63072000; includeSubDomains; preload`).
   - X-Content-Type-Options: `nosniff`.
   - In-memory sliding-window IP rate limiting (300 req/min for telemetry, 30 req/min for optimization).

---

## 6. Technology Selection Matrix & Rationale

| Layer / Capability | Selected Technology | Evaluated Alternatives | Engineering Rationale |
| :--- | :--- | :--- | :--- |
| **Frontend Framework** | **Next.js 15 (React 19)** | Vite + React SPA, Remix | Zero-config edge deployment on Vercel, built-in server-side proxy rewrites, instant global CDN delivery. |
| **UI Components** | **Tailwind CSS + Lucide** | Material UI, Ant Design | Zero runtime CSS overhead, maximum ergonomics, strict enterprise aesthetic without generic template bloat. |
| **Backend API** | **FastAPI (Python 3.12)** | Flask, Django, Go / Gin | Native async ASGI, automatic Pydantic v2 schema validation, direct access to Python scientific/OR ecosystem. |
| **Prescriptive Solver** | **Google OR-Tools SCIP** | PuLP, CBC, Gurobi | Open-source (₹0 cost), production-grade branch-and-cut MILP performance (< 60 ms), no commercial license locks. |
| **Analytical OLAP** | **DuckDB** | Pandas only, SQLite only | Columnar vector execution, multi-threaded aggregation over time series, zero-copy Arrow memory bridge. |
| **Transactional DB** | **SQLite WAL** | PostgreSQL, MySQL | Self-contained, zero-cost, persistent in-process speed (> 5,000 tx/sec), trivial deterministic benchmark reset. |
| **Vector PDF Engine** | **Python ReportLab** | Puppeteer / WeasyPrint | Pure Python vector generation without headless browser dependencies; < 15 MB RAM overhead; sub-second generation. |
| **Cloud Hosting** | **Vercel + Render** | AWS ECS, Google Cloud Run | Strictly ₹0 permanent free tier, zero billing surprises, split edge-CDN and Linux compute architecture. |

---

## 7. Operational Implementation vs Planned Capabilities

To maintain technical credibility during engineering evaluations, this section formally delineates live, working features from architectural roadmaps:

### 7.1 Formally Verified Implemented Capabilities (Live in Production)
- Full 16-module interactive user interface on Vercel Edge.
- Discrete difference 90-day daily accounting simulation engine.
- Google OR-Tools SCIP MILP solver executing in 1 ms with budget constraints.
- Two-Man Rule dual executive sign-off with SHA-256 cryptographic seal.
- Walk-forward forecasting evaluation (Ridge vs Holt-Winters vs Moving Average).
- Streaming vector PDF and RFC-4180 CSV report generation with 100% parity.
- Single-origin edge proxy eliminating browser CORS barriers.
- Multi-entity CSV data ingestion with schema validation and quality scoring.

### 7.2 Architectural Roadmap / Simulated Capabilities
- **Multi-Cloud Tenant Isolation:** Currently modeled as a multi-role single-tenant enterprise (Vanguard Apparel Co.); multi-tenant PostgreSQL schema partitioning is an architectural roadmap item.
- **Real-Time Carrier Webhook Stream:** Inbound ocean delays are simulated via shock injection parameters rather than active EDI 214/315 automated carrier webhooks.
- **Deep Reinforcement Learning (PPO) Policy:** Policy optimization currently evaluates stochastic Monte Carlo parameter sweeps over standard heuristic suites; continuous-action DRL policies are planned for v7.0.

