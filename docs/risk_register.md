# ENTERPRISE RISK REGISTER & MITIGATION MATRIX

**Document ID:** RISK-ATLAS-001  
**Version:** 1.0.0  
**Phase:** Phase 0 Baseline  
**Author:** Technical Program Manager & Senior Risk Architect  

---

## 1. Risk Governance & Assessment Methodology

SARAS ATLAS employs a standard qualitative Risk Severity Matrix based on **Likelihood (1–5)** and **Impact (1–5)**, resulting in a compound Risk Score ($1 \le R \le 25$):
- **Critical Risk ($R \ge 15$):** Immediate architectural mitigation required; blocks release gates.
- **Moderate Risk ($8 \le R \le 14$):** Active monitoring and automated guardrails enforced.
- **Low Risk ($R \le 7$):** Routine observation and operational logging.

---

## 2. Comprehensive Risk Assessment Matrix

```
+----------------------------------------------------------------------------------------------------+
|                                    SARAS ATLAS RISK REGISTER                                       |
+-----+-----------------------+-----+-----+----+----------+------------------------------------------+
| ID  | Risk Description      | L   | I   | R  | Severity | Architectural Mitigation Strategy        |
+-----+-----------------------+-----+-----+----+----------+------------------------------------------+
| R01 | 8 GB RAM Host Ceiling | 5   | 4   | 20 | CRITICAL | In-process modular monolith; SQLite WAL; |
|     | Memory Starvation     |     |     |    |          | DuckDB; zero background server daemons.  |
+-----+-----------------------+-----+-----+----+----------+------------------------------------------+
| R02 | Zero-Budget API Token | 5   | 3   | 15 | CRITICAL | Zero paid LLMs; deterministic variance   |
|     | Expense Breach (₹0)   |     |     |    |          | narrative templates; local MILP solver.  |
+-----+-----------------------+-----+-----+----+----------+------------------------------------------+
| R03 | Combinatorial Solver  | 2   | 4   | 8  | MODERATE | Hard 3.0-second timeout ceiling; returns |
|     | Explosion / Timeout   |     |     |    |          | best feasible integer solution.          |
+-----+-----------------------+-----+-----+----+----------+------------------------------------------+
| R04 | Non-Deterministic     | 4   | 5   | 20 | CRITICAL | Pure mathematical GAAP formulas; zero    |
|     | LLM Math Hallucination|     |     |    |          | LLM-based arithmetic allowed in core.    |
+-----+-----------------------+-----+-----+----+----------+------------------------------------------+
| R05 | Confusion Regarding   | 2   | 5   | 10 | MODERATE | Mandatory legal disclaimers on every doc |
|     | Saras Affiliation     |     |     |    |          | and UI screen stating independent status.|
+-----+-----------------------+-----+-----+----+----------+------------------------------------------+
| R06 | Censored Demand Bias  | 3   | 4   | 12 | MODERATE | Tobit regression imputation reconstructing|
|     | on Stockout Days      |     |     |    |          | true latent demand during stockouts.     |
+-----+-----------------------+-----+-----+----+----------+------------------------------------------+
| R07 | Unauthorized Auto     | 1   | 5   | 5  | LOW      | Zero external financial API connections; |
|     | Financial Transactions|     |     |    |          | mandatory two-man cryptographic sign-off.|
+-----+-----------------------+-----+-----+----+----------+------------------------------------------+
| R08 | Python Host Version   | 4   | 3   | 12 | MODERATE | Pinned isolated virtualenv (.venv) to    |
|     | Fragmentation         |     |     |    |          | Python 3.12.10; direct executable calls. |
+-----+-----------------------+-----+-----+----+----------+------------------------------------------+
```

---

## 3. Deep-Dive Mitigation Plans for High-Impact Risks

### R01: 8 GB RAM Host Ceiling & Operating System Stability
- **Nature of Risk:** The host development machine has 8.0 GB physical RAM with ~1.73 GB free memory under baseline Windows 11 load. If application memory exceeds ~1.2 GB, Windows will page heavily to disk, degrading responsiveness and freezing developer tools.
- **Architectural Safeguards:**
  1. *No External Database Daemons:* Replaced standalone PostgreSQL server (which consumes 250MB+ constantly) with in-process SQLite WAL mode and embedded DuckDB.
  2. *No Local 7B/13B LLMs:* Eliminated local Ollama/Llama model runtimes (which require 4.5–6.0 GB RAM).
  3. *Vectorized NumPy Memory Slices:* State transition matrices allocate continuous C-contiguous memory blocks ($< 15\text{ MB}$ per 90-day simulation array).
  4. *Continuous Monitoring:* Health endpoint `/api/v1/health` logs resident set size (RSS) on every run.

### R04: Elimination of LLM Financial Calculation Hallucinations
- **Nature of Risk:** In many AI startups, language models are asked to evaluate business trade-offs, leading to fabricated margins, false arithmetic sums, and ungrounded advice that would cause catastrophic capital loss if followed by an enterprise.
- **Architectural Safeguards:**
  1. *Strict Structural Segregation:* The Python calculation core is completely isolated from any text-generation layer.
  2. *Audited Accounting Identities:* Net Contribution Margin, landed costs, carrier tariffs, and working capital follow explicit GAAP formulas verified down to the penny via automated Pytest suites.
  3. *Verifiable Optimization Proofs:* Recommendations are produced by Google OR-Tools using mixed-integer linear programming, providing mathematically provable optimal bounds rather than generative guesses.

### R05: Brand Integrity & Saras Analytics Legal Boundary
- **Nature of Risk:** Potential misunderstanding by external parties that SARAS ATLAS is an official, commissioned, or endorsed product of Saras Analytics.
- **Operational Safeguards:**
  1. Prominent legal disclaimers inserted into all documentation headers, README files, API health responses, and UI footers:  
     *"SARAS ATLAS is an independent innovation project. It has not been commissioned, endorsed, or sponsored by Saras Analytics, nor does it access any private Saras systems or proprietary client data."*
  2. Zero attempts to connect to or scrape internal or authenticated Saras systems.
  3. All Saras product evaluations cite public documentation and case studies labeled as company-reported.

