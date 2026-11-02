# SARAS ATLAS — ARCHITECTURE DECISION RECORDS (ADRs)

**Project:** SARAS ATLAS (Commerce Resilience & Decision Simulation Platform)  
**Status:** Approved for Phase 0 Baseline  
**Date:** November 2, 2026  

---

## Index of Architecture Decision Records

- [ADR-001: In-Process Dual Storage Strategy (SQLite + DuckDB via SQLAlchemy)](#adr-001-in-process-dual-storage-strategy)
- [ADR-002: Modular Monolith Architecture vs Distributed Microservices](#adr-002-modular-monolith-architecture)
- [ADR-003: 100% Deterministic Simulation Core Free from LLM Hallucinations](#adr-003-deterministic-simulation-core)
- [ADR-004: Frontend Stack (Next.js 15 App Router, React 19, Tailwind CSS, Recharts)](#adr-004-frontend-technology-stack)
- [ADR-005: Backend Framework (Python 3.12, FastAPI, Pydantic v2, Asyncio)](#adr-005-backend-framework)
- [ADR-006: Optimization Engine Selection (Google OR-Tools MILP)](#adr-006-optimization-engine-selection)
- [ADR-007: Graph & Network Propagation Modeling (NetworkX Directed Acyclic Multigraph)](#adr-007-graph--network-propagation-modeling)
- [ADR-008: Zero-Cost AI Explainability Strategy via Rule-Based Template Generators](#adr-008-zero-cost-ai-explainability-strategy)

---

### ADR-001: In-Process Dual Storage Strategy
- **Context:** The development laptop has 8 GB physical RAM with ~1.7 GB free memory. Installing and running a PostgreSQL 17 Windows service with pgAdmin 4 adds background resident memory pressure (250–400 MB RAM continuously), requires elevated admin privileges for background service installation, and opens listening network ports.
- **Decision:** Adopt an in-process dual-engine storage strategy:
  1. **Transactional Engine (OLTP):** SQLite 3 (WAL mode enabled, foreign keys enforced) abstracted via **SQLAlchemy 2.0 ORM** with **Alembic** migrations.
  2. **Analytical & Simulation Engine (OLAP):** **DuckDB** embedded analytical database for vectorized aggregations, multi-scenario counterfactual joins, and fast parquet ingestion.
- **Consequences:**
  - *Positive:* 0 MB RAM consumption when application is idle; zero network port attack surface; zero installation barriers; zero background services.
  - *Positive:* 100% dialect portability. Because all schemas and relationships are defined in standard SQLAlchemy 2.0 declarative models, upgrading to a cloud PostgreSQL instance in production requires changing only the `DATABASE_URL` connection string.
  - *Negative:* SQLite has write-locking concurrency limits under intense simultaneous write bursts. For local single-operator simulation and demonstration, this is entirely negligible.

---

### ADR-002: Modular Monolith Architecture
- **Context:** Modern enterprise platforms often prematurely decouple into microservices (Auth service, Inventory service, Simulation service, Optimization service), introducing Docker overhead, network serialization latency, distributed tracing complexity, and significant memory overhead (each Python container consuming 150+ MB base memory).
- **Decision:** Build SARAS ATLAS as a unified **Modular Monolith**. 
  - Modules are strictly separated by domain boundaries inside the backend package: `domain/twin`, `domain/simulation`, `domain/optimization`, `domain/financials`, `domain/governance`.
  - In-process communication via typed domain service interfaces and event dispatchers.
- **Consequences:**
  - *Positive:* Runs within a single Python process consuming < 250 MB RAM. Zero network serialization between twin state and optimization engine. Fast in-memory object passing.
  - *Positive:* Ultra-fast development cadence, instant test execution via Pytest, effortless refactoring.
  - *Negative:* Modules must be disciplined to avoid circular dependencies. Enforced via strict linting and interface boundaries.

---

### ADR-003: Deterministic Simulation Core
- **Context:** Many contemporary "AI agents" attempt to compute financial projections, inventory levels, and logistics trade-offs using Large Language Models (LLMs). LLMs are non-deterministic, prone to calculation hallucinations, incapable of exact constraint programming, and financially expensive.
- **Decision:** Every calculation, metric, impact propagation, financial statement, and simulation in SARAS ATLAS is **100% deterministic, mathematically verified, and grounded in explicit accounting and inventory formulas**.
  - Inventory coverage = Deterministic formula ($I_t / \bar{D}_t$).
  - Contribution Margin = Exact GAAP unit economics equation ($P - COGS - PickPack - Shipping - AdSpend$).
  - Constraint optimization = Mixed-Integer Linear Programming (MILP) solved via Google OR-Tools.
  - AI/LLM layers (if enabled) are strictly relegated to *synthesizing natural language explanations, drafting executive briefings, and explaining the mathematical output of the deterministic core*.
- **Consequences:**
  - *Positive:* Complete enterprise auditability, zero financial hallucination risk, instantaneous calculation speeds (< 50ms), runs 100% offline at ₹0 cost.
  - *Positive:* Defensible before CFOs, CTOs, and technical founders.

---

### ADR-004: Frontend Technology Stack
- **Context:** The frontend must render executive-grade business dashboards, complex network graphs (supply chain topologies), interactive scenario comparison tables, and sensitivity sliders with sub-second feedback.
- **Decision:** **Next.js 15 (React 19, TypeScript, Tailwind CSS)** with:
  - Component library: Accessible Tailwind/Radix primitives (shadcn-inspired).
  - Data visualization: Recharts for financial and inventory charts; Lucide-React for clean iconography.
  - Network Graph: ReactFlow / SVG-based interactive canvas for multi-echelon supply chain visualization.
- **Consequences:**
  - *Positive:* Industry-standard TypeScript type safety sharing schema types with backend Pydantic models. Lightning-fast client rendering.
  - *Negative:* Requires Node.js build process. (Verified: Node v24.15.0 and npm 11.17.0 are already present).

---

### ADR-005: Backend Framework
- **Context:** The backend must handle REST endpoints for the web UI, perform multi-scenario mathematical calculations, interface with tabular dataframes, and support async execution.
- **Decision:** **Python 3.12 + FastAPI + Pydantic v2 + Asyncio**.
- **Consequences:**
  - *Positive:* Automated OpenAPI (Swagger) documentation; Pydantic v2 core compiled in Rust for lightning-fast schema validation; seamless interop with NumPy, SciPy, Statsmodels, and OR-Tools.
  - *Positive:* Native support in Python 3.12 with enhanced error tracebacks and performance gains.

---

### ADR-006: Optimization Engine Selection
- **Context:** The platform must recommend optimal decisions (e.g. how many units of SKU A to air-freight vs ocean-freight, how to reallocate stock across 3 regional 3PLs, and how to adjust ad spend to maximize Contribution Margin without running out of cash).
- **Decision:** Adopt **Google OR-Tools (Operations Research Tools)** Mixed-Integer Linear Programming (MILP) solver (CBC / SCIP / GLOP).
- **Consequences:**
  - *Positive:* Open-source, Apache 2.0 licensed, zero-cost, enterprise-proven optimization library. Finds mathematically provable global optima given objective functions and linear constraints.
  - *Negative:* Requires formulating business decisions into strict linear/integer constraints. Well within engineering capabilities.

---

### ADR-007: Graph & Network Propagation Modeling
- **Context:** Commerce operational disruptions propagate through a network: Supplier $\rightarrow$ Port $\rightarrow$ Customs $\rightarrow$ Central Hub $\rightarrow$ Regional 3PL $\rightarrow$ Customer Orders. We need to model dependency edges, lead-time delays, and bottleneck nodes.
- **Decision:** Use **NetworkX** for directed acyclic multigraph representation of the supply chain network, combined with vectorized NumPy propagation arrays.
- **Consequences:**
  - *Positive:* Pure Python, zero-dependency, mathematically sound topological sorting and critical path analysis. Instant pathfinding and shock cascading.
  - *Negative:* In-memory only, but effortlessly handles up to 100,000 nodes—far exceeding mid-market supply chain topologies (typically 5–50 nodes).

---

### ADR-008: Zero-Cost AI Explainability Strategy
- **Context:** The prompt mandates ₹0 spending and zero paid AI APIs. However, business leaders expect executive natural language summaries explaining *why* a disruption occurred and *why* a particular decision is recommended.
- **Decision:** Implement a dual-mode Explainability Engine:
  1. **Deterministic Structured Narrative Synthesizer (Default / Zero-Cost):** Uses rule-based semantic templating, parametric narrative trees, and variance-decomposition algorithms to generate publication-grade executive briefs directly from calculated metrics.
  2. **Pluggable LLM Adapter (Optional / Future):** Abstracted interface (`LLMProviderInterface`) allowing seamless connection to local free models (via Ollama) or cloud providers if authorized in future phases.
- **Consequences:**
  - *Positive:* Guaranteed 100% uptime, zero token costs, instantaneous narrative generation, zero external API keys needed.
