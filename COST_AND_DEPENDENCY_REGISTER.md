# SARAS ATLAS — COST AND DEPENDENCY REGISTER

**Project:** SARAS ATLAS (Commerce Resilience & Decision Simulation Platform)  
**Budgetary Mandate:** ₹0 (Zero INR / Zero USD)  
**Financial Status:** 100% Zero-Cost Compliant  
**Date:** November 2, 2026  

---

## 1. Zero-Cost Budget Verification

| Expense Category | Allocated Budget | Incurred Cost | Projected Phase 1-4 Cost | Variance |
| :--- | :--- | :--- | :--- | :--- |
| **Compute & Cloud Hosting** | ₹0.00 | ₹0.00 (Localhost Windows 11) | ₹0.00 | ₹0.00 |
| **Database Licensing** | ₹0.00 | ₹0.00 (SQLite & DuckDB In-Process) | ₹0.00 | ₹0.00 |
| **AI / LLM API Tokens** | ₹0.00 | ₹0.00 (Deterministic Rule Engine) | ₹0.00 | ₹0.00 |
| **Software Tooling & IDEs** | ₹0.00 | ₹0.00 (Antigravity IDE / VS Code / Git) | ₹0.00 | ₹0.00 |
| **Third-Party SaaS Subscriptions** | ₹0.00 | ₹0.00 (Zero subscriptions) | ₹0.00 | ₹0.00 |
| **Domain & SSL Certificates** | ₹0.00 | ₹0.00 (Local development) | ₹0.00 | ₹0.00 |
| **Total Expenditure** | **₹0.00** | **₹0.00** | **₹0.00** | **₹0.00** |

---

## 2. Comprehensive Dependency Register & License Audit

Every selected dependency has been audited for license compliance (permissive open-source only: MIT, Apache 2.0, BSD), memory footprint, and architectural necessity.

### Backend Dependencies (Python 3.12)

| Package | Version Target | License | Memory Footprint | Commercial Use | Purpose / Justification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **fastapi** | `^0.115.0` | MIT | ~15 MB | Permitted | High-performance asynchronous REST API framework with automatic OpenAPI docs. |
| **uvicorn** | `^0.32.0` | BSD-3-Clause | ~10 MB | Permitted | Lightweight ASGI server for running FastAPI locally. |
| **pydantic** | `^2.9.0` | MIT | ~12 MB | Permitted | Rust-backed schema validation and settings management. Zero overhead. |
| **sqlalchemy** | `^2.0.36` | MIT | ~20 MB | Permitted | Enterprise relational ORM with dialect abstraction (SQLite $\rightarrow$ Postgres). |
| **alembic** | `^1.13.3` | MIT | ~5 MB | Permitted | Database schema migrations and versioning. |
| **duckdb** | `^1.1.2` | MIT | ~35 MB | Permitted | Embedded vectorized OLAP database for fast counterfactual query evaluation. |
| **numpy** | `^2.1.0` | BSD-3-Clause | ~25 MB | Permitted | Fundamental array operations and fast matrix calculations for shock propagation. |
| **pandas** | `^2.2.3` | BSD-3-Clause | ~40 MB | Permitted | Tabular data manipulation for synthetic data generation and export. |
| **scipy** | `^1.14.1` | BSD-3-Clause | ~45 MB | Permitted | Statistical distributions and piecewise optimization fallback. |
| **statsmodels** | `^0.14.4` | BSD-3-Clause | ~40 MB | Permitted | Classical time-series forecasting baselines (Exponential Smoothing, Holt-Winters). |
| **scikit-learn** | `^1.5.2` | BSD-3-Clause | ~45 MB | Permitted | Machine learning baselines for demand elasticities and regression models. |
| **ortools** | `^9.11.4210` | Apache-2.0 | ~50 MB | Permitted | Google Operations Research Tools (MILP solver) for inventory/shipping optimization. |
| **networkx** | `^3.4.2` | BSD-3-Clause | ~10 MB | Permitted | Directed graph representations for multi-echelon supply-chain network topologies. |
| **pytest** | `^8.3.3` | MIT | ~10 MB | Permitted | Robust unit and integration testing suite. |
| **httpx** | `^0.27.2` | BSD-3-Clause | ~8 MB | Permitted | Async HTTP client for FastAPI integration testing. |

*Combined backend peak memory:* ~325 MB RAM (Well within the 1.73 GB free physical limit).

### Frontend Dependencies (Node.js 24 / npm)

| Package | Version Target | License | Commercial Use | Purpose / Justification |
| :--- | :--- | :--- | :--- | :--- |
| **next** | `^15.0.0` | MIT | Permitted | Next.js App Router for server-rendered and client-rendered executive UI. |
| **react** / **react-dom** | `^19.0.0` | MIT | Permitted | Modern UI component rendering with concurrent features. |
| **typescript** | `^5.6.0` | Apache-2.0 | Permitted | Full static type safety across schemas, API payloads, and state stores. |
| **tailwindcss** | `^3.4.0` | MIT | Permitted | Utility-first responsive CSS styling with zero runtime stylesheet overhead. |
| **lucide-react** | `^0.454.0` | ISC | Permitted | Accessible, crisp icon library for commerce and supply chain visualizations. |
| **recharts** | `^2.13.0` | MIT | Permitted | Declarative, SVG-based responsive charting for inventory waterfalls and CM trends. |
| **zustand** | `^5.0.0` | MIT | Permitted | Ultra-lightweight (1 KB) client state management for scenario sliders and filters. |

*Combined frontend build & dev memory:* ~250 MB RAM during client interaction.

---

## 3. Explicit Prohibitions & Avoided Tooling

To uphold the strict ₹0 budget and 8 GB hardware bounds, the following tools were explicitly evaluated and rejected:
1. **OpenAI / Anthropic Paid Cloud APIs:** Rejected to maintain ₹0 mandate and prevent non-deterministic financial hallucinations.
2. **Local 7B/13B LLM Runtimes (e.g. Llama-3-8B via Ollama):** Rejected because loading an 8B model requires 4.5–6.0 GB RAM, which would immediately crash the host OS.
3. **Docker Desktop & Container Daemons:** Rejected due to 1.5–2.0 GB Windows WSL2/Hyper-V RAM reservation.
4. **Standalone PostgreSQL Windows Service:** Rejected due to persistent background daemon overhead when SQLite + DuckDB provide identical relational capability in-process.
5. **Redis Cache Daemon:** Rejected because in-memory Python `functools.lru_cache` and dictionary stores suffice for single-node local caching with 0 MB background cost.



---

## 3. Phase 1 Cost & License Audit Post-Execution

- **Total Incurred Cost in Phase 1:** **₹0.00**
- **Cloud/API Calls Made:** **0 calls**
- **Installed Packages Audit in `.venv`:**
  - `fastapi==0.115.14` (MIT)
  - `uvicorn==0.32.1` (BSD-3-Clause)
  - `pydantic==2.9.2` (MIT)
  - `sqlalchemy==2.0.55` (MIT)
  - `alembic==1.13.3` (MIT)
  - `duckdb==1.1.3` (MIT)
  - `numpy==2.1.3` (BSD-3-Clause)
  - `pandas==2.2.3` (BSD-3-Clause)
  - `scipy==1.14.1` (BSD-3-Clause)
  - `statsmodels==0.14.6` (BSD-3-Clause)
  - `scikit-learn==1.5.2` (BSD-3-Clause)
  - `ortools==9.11.4210` (Apache-2.0)
  - `networkx==3.4.2` (BSD-3-Clause)
  - `pytest==8.3.5` (MIT)
  - `httpx==0.27.2` (BSD-3-Clause)
- **Host RAM Consumption Audited:** **96.77 MB RSS** peak during combined simulation and optimization solves.
- **Compliance Status:** **100% COMPLIANT WITH ₹0 BUDGET & 8 GB RAM LIMITS**.

---

## 4. Phase 2 Cost & License Audit Post-Execution

- **Total Incurred Cost in Phase 2:** **₹0.00**
- **Cumulative Project Incurred Cost:** **₹0.00**
- **Cloud/API Calls Made:** **0 calls** (Zero paid LLMs, zero paid APIs)
- **Frontend Dependencies Audit in `frontend/package.json`:**
  - `next==15.1.7` (MIT)
  - `react==19.0.0` (MIT)
  - `react-dom==19.0.0` (MIT)
  - `recharts==2.15.1` (MIT)
  - `lucide-react==0.475.0` (ISC / MIT equivalent)
  - `clsx==2.1.1` (MIT)
  - `tailwind-merge==3.0.1` (MIT)
  - `tailwindcss==3.4.17` (MIT)
  - `typescript==5.7.3` (Apache-2.0)
- **Client Bundle Size:** **131 kB** (Route `/`)
- **Background Processes Running:** **0 persistent background daemons** (All servers terminated post-testing and screenshot capture)
- **Compliance Status:** **100% COMPLIANT WITH ₹0 BUDGET & 8 GB RAM LIMITS**.

---

## 5. Phase 3 Cost & License Audit Post-Execution

- **Total Incurred Cost in Phase 3:** **₹0.00**
- **Cumulative Project Incurred Cost (Phases 0–3):** **₹0.00**
- **Cloud/API Calls Made:** **0 calls** (Zero paid LLMs, zero paid cloud services)
- **Added Backend Dependencies in `requirements.txt`:**
  - `openpyxl==3.1.5` (MIT License) — Ingest and parse Excel `.xlsx` spreadsheets locally without Microsoft Office.
  - `python-multipart==0.0.33` (Apache-2.0 License) — Standard streaming multipart parser for FastAPI file uploads.
- **Client Bundle Size After Phase 3 Expansion:** **143 kB** (Route `/` with 13 enterprise modules)
- **Host RAM Working Set Audited:** **94.89 MB RSS** peak during 100-scenario batch execution.
- **Background Processes Running:** **0 persistent background daemons** (FastAPI and Next.js launched only on demand; zero background daemons running).
- **Compliance Status:** **100% COMPLIANT WITH ₹0 BUDGET & 8 GB RAM LIMITS**.
