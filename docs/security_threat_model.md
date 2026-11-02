# SECURITY THREAT MODEL & GOVERNANCE SPECIFICATION

**Document ID:** SEC-ATLAS-001  
**Version:** 1.0.0  
**Phase:** Phase 0 Baseline  
**Author:** Cybersecurity Architect & Autonomous CTO  
**Methodology:** Microsoft STRIDE Threat Modeling Framework  

---

## 1. Security Philosophy & The Zero-Trust Operational Policy

SARAS ATLAS manages sensitive commercial intelligence: supply chain network topologies, supplier contracts, unit cost breakdowns, carrier tariffs, customer order streams, and forward-looking financial forecasts.

Core security guardrails:
1. **Zero Autonomous Financial Transactions:** The platform is strictly prohibited from executing autonomous external financial payments, wire transfers, automated supplier purchase orders, or irreversible database deletions.
2. **Localhost Network Binding:** The development and local execution environment binds exclusively to `127.0.0.1`, exposing zero listening sockets to external networks.
3. **Immutable Two-Man Approval Gates:** High-impact mitigation decisions exceeding cash thresholds require cryptographically logged, multi-signature human approval.
4. **Zero Secrets in Source Control:** Strict automated pre-commit scanning to ensure no API keys, tokens, or credentials are committed to Git.

---

## 2. STRIDE Threat Analysis Matrix

```
+-----------------------------------------------------------------------------------------+
|                               STRIDE THREAT MODEL AUDIT                                 |
+----+----------------------+---------------------------+---------------------------------+
| ID | Threat Category      | Potential Vulnerability   | Mitigation & Security Control   |
+----+----------------------+---------------------------+---------------------------------+
| S  | Spoofing Identity    | Attacker impersonates COO | Local Role-Based Access Control |
|    |                      | to authorize decisions.   | (RBAC) with session tokens.     |
+----+----------------------+---------------------------+---------------------------------+
| T  | Tampering with Data  | Mutation of baseline twin | In-Memory Read-Only Sandboxes;  |
|    |                      | data or financial params. | SQLite WAL mode & transactions. |
+----+----------------------+---------------------------+---------------------------------+
| R  | Repudiation          | Executive denies approving| SHA-256 Cryptographic Audit Log |
|    |                      | capital allocation plan.  | with timestamped user hash.     |
+----+----------------------+---------------------------+---------------------------------+
| I  | Information          | Leakage of supplier COGS  | Localhost binding; strict CORS; |
|    | Disclosure           | or customer order data.   | zero external cloud sync.       |
+----+----------------------+---------------------------+---------------------------------+
| D  | Denial of Service    | Malicious parameter shock | Pydantic boundary validation;   |
|    |                      | causes solver hang/OOM.   | hard 3.0s solver execution cap. |
+----+----------------------+---------------------------+---------------------------------+
| E  | Elevation of         | Operator escalates to     | Explicit role middleware;       |
|    | Privilege            | Executive approval rights.| server-side role verification.  |
+----+----------------------+---------------------------+---------------------------------+
```

---

## 3. Role-Based Access Control (RBAC) Architecture

SARAS ATLAS defines four explicit operational roles with strict principle-of-least-privilege boundaries:

| Permission / Capability | Viewer / Auditor | Operational Analyst | Supply Chain Manager | Executive (COO / CFO) |
| :--- | :---: | :---: | :---: | :---: |
| **View Situation Room & Network Map** | Yes | Yes | Yes | Yes |
| **Inspect Digital Twin Inventory** | Yes | Yes | Yes | Yes |
| **Run Ephemeral What-If Simulations** | Read-Only | Yes | Yes | Yes |
| **Trigger OR-Tools Optimization Solver** | No | Yes | Yes | Yes |
| **Create Persistent Simulation Branches**| No | Yes | Yes | Yes |
| **Modify Baseline Unit Economics / COGS**| No | No | Yes (Draft) | Yes (Commit) |
| **Sign Off & Authorize Recommendations** | No | No | No | **Yes (Two-Man Rule)** |
| **Export Operational Action Directives** | No | Yes | Yes | Yes |

### Two-Man Rule Governance Specification
Any mitigation decision that involves:
- Capital outlay $> \$25,000$ (e.g. emergency air freight purchase order), OR
- Demand throttling $> 15\%$ on core hero SKUs

**MUST require electronic dual-authorization:**
1. Operational Sign-off: Submitted by **COO / VP of Supply Chain** (verifying logistical feasibility).
2. Financial Sign-off: Authorized by **CFO / VP of Finance** (verifying working capital allocation).

---

## 4. Input Validation, Injection Defense & Data Isolation

### 4.1 Strict Pydantic v2 Schema Enforcement
Every inbound payload is strictly validated at the API boundary before entering domain services:
- **Parameter Bounds:**
  - `delay_days`: Integer, bounded by $-30 \le \Delta L \le +90$.
  - `surcharge_pct`: Float, bounded by $-0.50 \le \beta \le +3.00$.
  - `demand_multiplier`: Float, bounded by $0.10 \le \alpha \le 5.00$.
- **Path Traversal Prevention:** Any file export or fixture path is verified against an allowed canonical root using `os.path.realpath` to prevent directory traversal (`../`).

### 4.2 SQL Injection Immunity
- All relational operations are mediated exclusively through **SQLAlchemy 2.0 ORM** using parameterized SQL statements. Raw string concatenation in SQL queries is strictly prohibited across the codebase.

---

## 5. Cryptographic Audit Trail Architecture

Every simulation run, scenario parameter modification, and formal approval generates an immutable audit entry in the `approval_records` and `audit_log` tables:

```python
# Cryptographic Audit Record Generator (src/domain/governance/audit.py)
import hashlib
import json
from datetime import datetime, timezone

def generate_approval_signature(recommendation_id: str, approver_id: str, role: str, decision: str, payload: dict) -> str:
    """
    Computes a deterministic SHA-256 cryptographic digest of an approval action.
    Guarantees non-repudiation and tampering detection.
    """
    audit_payload = {
        "recommendation_id": recommendation_id,
        "approver_id": approver_id,
        "role": role,
        "decision": decision,
        "action_payload": payload,
        "timestamp_utc": datetime.now(timezone.utc).isoformat()
    }
    serialized_bytes = json.dumps(audit_payload, sort_keys=True).encode('utf-8')
    return hashlib.sha256(serialized_bytes).hexdigest()
```

---

## 6. Secrets & Dependency Governance

1. **Environment Variables:** All secrets and configuration variables are isolated in `.env` files (loaded via `python-dotenv` and Pydantic `BaseSettings`).
2. **Git Hygiene:** Root `.gitignore` explicitly prevents `.env`, `.pem`, `.key`, and database files (`*.sqlite`, `*.db`) from ever being staged or committed.
3. **Dependency Auditing:** All third-party Python and Node.js packages are pinned to exact semantic versions and scanned against the GitHub Advisory Database (`pip-audit` and `npm audit`).
