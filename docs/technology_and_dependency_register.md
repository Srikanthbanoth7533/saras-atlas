# TECHNOLOGY & DEPENDENCY REGISTER

**Document ID:** TECH-ATLAS-001  
**Version:** 1.0.0  
**Phase:** Phase 0 Baseline  
**Author:** DevOps Engineer & Senior Systems Architect  

---

## 1. System Runtime & Toolchain Registry

| Technology / Binary | Verified Host Path | Exact Version | License | Installation Status |
| :--- | :--- | :--- | :--- | :--- |
| **Operating System** | `C:\WINDOWS` | Windows 11 Home 64-bit (Build 26300) | Microsoft Commercial | Pre-installed |
| **Host Processor** | CPU Socket | 11th Gen Intel Core i5-11320H (4C / 8T) | — | Hardware |
| **Physical Memory** | DIMM Slots (2x 4GB) | 8.0 GB LPDDR4x @ 4267 MHz | — | Hardware (Audited) |
| **Git SCM** | `C:\Program Files\Git\cmd\git.exe` | 2.54.0.windows.1 | GPL-2.0 / LGPL | Pre-installed & Verified |
| **Node.js Runtime** | `C:\Program Files\nodejs\node.exe` | v24.15.0 (V8 12.9) | MIT | Pre-installed & Verified |
| **npm Package Mgr** | `C:\Program Files\nodejs\npm.cmd` | 11.17.0 | Artistic-2.0 | Pre-installed & Verified |
| **Python LTS Runtime** | `C:\Users\DELL\AppData\Local\Python\pythoncore-3.12-64\python.exe` | 3.12.10 (64-bit) | PSF License | Pre-installed & Verified |
| **Python Virtualenv** | `C:\Users\DELL\.gemini\antigravity\scratch\saras-atlas\.venv` | Isolated 3.12.10 | PSF License | Provisioned in Phase 0 |
| **pip Installer** | `saras-atlas\.venv\Scripts\pip.exe` | 25.0.1 | MIT | Provisioned in Phase 0 |
| **Package Manager** | `C:\Users\DELL\AppData\Local\Microsoft\WindowsApps\winget.exe` | v1.29.380 | MIT | Pre-installed & Verified |

---

## 2. Backend Dependency Register (Python 3.12)

All packages are pinned in `requirements.txt` and verified compatible with Python 3.12 64-bit:

```
# Core Web API & Validation
fastapi==0.115.4
uvicorn[standard]==0.32.0
pydantic==2.9.2
pydantic-settings==2.6.1

# Relational & Analytical In-Process Storage
sqlalchemy==2.0.36
alembic==1.13.3
duckdb==1.1.2

# Numerical & Operations Research
numpy==2.1.2
pandas==2.2.3
scipy==1.14.1
statsmodels==0.14.4
scikit-learn==1.5.2
ortools==9.11.4210
networkx==3.4.2

# Testing & Utilities
pytest==8.3.3
pytest-asyncio==0.24.0
httpx==0.27.2
python-dotenv==1.0.1
```

### Detailed Package Evaluation

| Library | Version | License | Estimated Memory | System Function / Justification |
| :--- | :--- | :--- | :--- | :--- |
| **FastAPI** | 0.115.4 | MIT | ~15 MB | High-concurrency async REST API router with automated OpenAPI specs. |
| **Uvicorn** | 0.32.0 | BSD-3-Clause | ~10 MB | Ultra-fast ASGI web server for local API hosting. |
| **Pydantic** | 2.9.2 | MIT | ~12 MB | Rust-compiled validation core. Enforces strict types and parameter boundaries. |
| **SQLAlchemy** | 2.0.36 | MIT | ~20 MB | Modern 2.0 ORM managing SQLite schema, transactions, and foreign keys. |
| **DuckDB** | 1.1.2 | MIT | ~35 MB | Embedded columnar OLAP engine for vectorized multi-scenario analytics. |
| **NumPy** | 2.1.2 | BSD-3-Clause | ~25 MB | High-speed C-array operations powering the discrete simulation engine. |
| **Pandas** | 2.2.3 | BSD-3-Clause | ~40 MB | Tabular manipulation for synthetic dataset generation and CSV/Parquet export. |
| **SciPy** | 1.14.1 | BSD-3-Clause | ~45 MB | Scientific distributions for stochastic lead times and normal CDF calculations. |
| **Statsmodels** | 0.14.4 | BSD-3-Clause | ~40 MB | Classical statistical forecasting (Holt-Winters Triple Exponential Smoothing). |
| **Scikit-learn**| 1.5.2 | BSD-3-Clause | ~45 MB | Quantile regression and machine learning baseline feature models. |
| **OR-Tools** | 9.11.4210 | Apache-2.0 | ~50 MB | Google Operations Research Suite (SCIP/CBC MILP decision solver). |
| **NetworkX** | 3.4.2 | BSD-3-Clause | ~10 MB | Directed multigraph modeling of multi-echelon supply-chain network topologies. |
| **Pytest** | 8.3.3 | MIT | ~10 MB | Comprehensive unit and integration test runner. |
| **HTTPX** | 0.27.2 | BSD-3-Clause | ~8 MB | Asynchronous HTTP client for end-to-end API testing. |

---

## 3. Frontend Dependency Register (Next.js 15 / React 19)

All packages managed via `package.json` in the frontend directory:

```json
{
  "name": "saras-atlas-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^15.0.2",
    "react": "^19.0.0-rc",
    "react-dom": "^19.0.0-rc",
    "tailwindcss": "^3.4.14",
    "lucide-react": "^0.454.0",
    "recharts": "^2.13.3",
    "zustand": "^5.0.1",
    "clsx": "^2.1.1",
    "tailwind-merge": "^2.5.4"
  },
  "devDependencies": {
    "typescript": "^5.6.3",
    "@types/node": "^22.8.7",
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "postcss": "^8.4.47",
    "autoprefixer": "^10.4.20"
  }
}
```

---

## 4. Verification & Validation Protocol

The development environment can be verified at any time using our dedicated PowerShell script:
```powershell
# Verification Command:
powershell -ExecutionPolicy Bypass -File .\scripts\verify_environment.ps1
```
Which checks:
1. Active Python virtual environment (.venv) and version (Python 3.12.10).
2. Node.js version (v24.15.0) and npm version (11.17.0).
3. Git status and repository hygiene.
4. Total available memory headroom ($\ge 1.5\text{ GB}$).
