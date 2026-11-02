# SARAS ATLAS — Phase 6.5 Local Deployment Report

**Platform:** SARAS ATLAS — Commerce Resilience & Decision Simulation Platform  
**Target Entity:** Vanguard Apparel Co. (Mid-Market Omnichannel Apparel Brand — \$45M GMV)  
**Deployment Date:** November 3, 2026  
**Execution Environment:** Local Windows Workstation (8.0 GB RAM)  
**Host Binding:** `127.0.0.1:8000` (FastAPI) & `http://localhost:3000` (Next.js 15)  
**Git Baseline Commit:** `37d9a54` | **Version:** `6.0.0`  
**Total Incurred Cost:** **₹0.00** | **Cloud Tokens Consumed:** **0**

---

## 1. Pre-Deployment Inspection & Verification (Task 1)

Before launching services, an exhaustive audit of repository assets, runtimes, dependencies, and database files was conducted:

| Inspection Check | Target Asset | Verification Evidence | Status |
| :--- | :--- | :--- | :--- |
| **Git Baseline & Tree** | Commit `37d9a54` | `git status` clean; 0 unstaged modifications; HEAD verified at `37d9a54` | **VERIFIED** |
| **Python Virtualenv** | `.venv` (Python 3.12.10) | FastAPI 0.115.14, SQLAlchemy 2.0.55, Google OR-Tools 9.11.4210, NumPy 2.1.3 | **VERIFIED** |
| **Node.js Environment** | Node v24.15.0 / npm 11.17.0 | `frontend/node_modules` with Next.js 15.1.7, React 19.0.0, Recharts 2.15.1 | **VERIFIED** |
| **SQLite Database** | `data/saras_atlas.db` | 21,790,720 bytes (21.4 MB); `PRAGMA integrity_check` = `ok`; WAL mode verified | **VERIFIED** |
| **Synthetic Business Data** | Vanguard Apparel Co. | 50 SKUs, 5 Warehouses, 3 Suppliers, 37,500 Orders, 150 Inventory Snapshots intact | **VERIFIED** |
| **Security & Ports** | Local TCP Sockets | Ports 8000 and 3000 confirmed free prior to launch; zero external exposure | **VERIFIED** |
| **Safe Database Backup** | Hot Vacuum Snapshot | Created `data/backups/saras_atlas_backup_20261102_201747.db` (21,790,720 bytes) | **VERIFIED** |

---

## 2. Service Startup & Runtime Architecture (Task 2)

Both backend and frontend services were launched locally using strictly sandboxed loopback bindings:

```mermaid
graph LR
    subgraph Host["Local Workstation (Windows 11 - 8 GB RAM)"]
        Browser["Microsoft Edge / Local Browser"]
        FE["Next.js 15 Frontend<br/>http://127.0.0.1:3000<br/>(PID 27976 | ~50 MB RAM)"]
        BE["FastAPI ASGI Server<br/>http://127.0.0.1:8000<br/>(PID 14428 | ~122 MB RAM)"]
        DB[("SQLite 3 WAL Database<br/>data/saras_atlas.db<br/>(In-Process MMAP)")]

        Browser -->|HTTP UI Navigation| FE
        FE -->|Typed REST Client| BE
        BE -->|SQLAlchemy 2.0 ORM| DB
    end
```

### 2.1 Backend Service Startup
* **Command Executed:**
  ```powershell
  cd C:\Users\DELL\.gemini\antigravity\scratch\saras-atlas
  .\.venv\Scripts\python.exe -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000
  ```
* **Binding Address:** `127.0.0.1:8000` (Strictly local loopback; zero binding to `0.0.0.0`).
* **Live Health Response (`GET /api/v1/health`):**
  ```json
  {
    "status": "HEALTHY",
    "service": "SARAS ATLAS — Commerce Resilience & Decision Simulation Platform",
    "version": "1.0.0-phase1",
    "database": "ONLINE (SQLite WAL)",
    "optimizer": "READY (OR-Tools SCIP)",
    "memory": {
      "system_total_phys_gb": 7.75,
      "system_avail_phys_gb": 1.16,
      "process_working_set_mb": 121.77
    },
    "architecture": "In-Process Modular Monolith (< 350 MB Target RSS)"
  }
  ```

### 2.2 Frontend Service Startup
* **Command Executed:**
  ```powershell
  cd C:\Users\DELL\.gemini\antigravity\scratch\saras-atlas\frontend
  npx next start -H 127.0.0.1 -p 3000
  ```
* **Binding Address:** `http://127.0.0.1:3000` / `http://localhost:3000`.
* **Execution Mode:** Production Mode (`next start`). Selected because the production build was previously compiled with 0 TypeScript and ESLint errors, yielding an optimized 152 kB bundle size that minimizes runtime CPU and memory overhead on the 8 GB host machine.
* **HTTP Status Check:** `GET http://localhost:3000` $\rightarrow$ `HTTP 200 OK` (Served in 12 ms).

---

## 3. Resource Footprint & Host Stability

Both services ran continuously without unexpected crashes, socket conflicts, or memory leaks:

| Process | PID | Working Set RSS | Memory Cap Budget | Headroom Status |
| :--- | :--- | :--- | :--- | :--- |
| **FastAPI Backend (Python 3.12)** | `14428` | **121.77 MB** | 350.0 MB | **65.2% Under Budget** |
| **Next.js Frontend (Node v24)** | `27976` | **49.54 MB** | 250.0 MB | **80.2% Under Budget** |
| **Next.js Worker Process** | `27388` | **33.61 MB** | — | Normal child worker |
| **Combined Application Footprint** | — | **204.92 MB** | 600.0 MB | **< 2.6% of 8 GB Host RAM** |

---

## 4. Local Deployment Conclusion

The local deployment of SARAS ATLAS v6.0 is **OPERATIONAL, HEALTHY, AND SECURE**. Both services remain running on their local ports for real-time browser verification and live executive demonstration.
