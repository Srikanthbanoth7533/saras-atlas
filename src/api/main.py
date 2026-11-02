"""
SARAS ATLAS — Enterprise REST API.
Commerce Resilience & Decision Simulation Platform.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.config import settings
from src.api.middleware.security import SecurityHeadersMiddleware, RateLimitingMiddleware
from src.api.routes import (
    health,
    twin,
    risks,
    simulation,
    optimization,
    governance,
    batch,
    policy,
    ingestion,
    auth,
    intelligence,
    rca,
    explainability,
    forecasting,
    connectors,
    reports,
    security,
)

app = FastAPI(
    title="SARAS ATLAS API",
    description=(
        "Enterprise Digital Twin & Decision Simulation Platform for E-Commerce and Retail. "
        "Provides multi-echelon network topology, operational risk detection, 90-day discrete "
        "difference scenario simulation, Google OR-Tools MILP prescriptive optimization, "
        "AI Decision Intelligence, Root Cause Analysis, Advanced Time-Series Forecasting, "
        "Enterprise Warehouse Connectors, and Executive Reporting with Two-Man Rule Governance."
    ),
    version="1.4.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Enforce Enterprise Security & Rate Limiting Middleware
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitingMiddleware)

# Enable CORS for local and web UI clients
origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",") if o.strip()]
if not origins:
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API v1 Routers
api_v1_prefix = "/api/v1"
app.include_router(health.router, prefix=api_v1_prefix)
app.include_router(twin.router, prefix=api_v1_prefix)
app.include_router(risks.router, prefix=api_v1_prefix)
app.include_router(simulation.router, prefix=api_v1_prefix)
app.include_router(optimization.router, prefix=api_v1_prefix)
app.include_router(governance.router, prefix=api_v1_prefix)
app.include_router(batch.router, prefix=api_v1_prefix)
app.include_router(policy.router, prefix=api_v1_prefix)
app.include_router(ingestion.router, prefix=api_v1_prefix)
app.include_router(auth.router, prefix=api_v1_prefix)
app.include_router(intelligence.router, prefix=api_v1_prefix)
app.include_router(rca.router, prefix=api_v1_prefix)
app.include_router(explainability.router, prefix=api_v1_prefix)
app.include_router(forecasting.router, prefix=api_v1_prefix)
app.include_router(connectors.router, prefix=api_v1_prefix)
app.include_router(reports.router, prefix=api_v1_prefix)
app.include_router(security.router, prefix=api_v1_prefix)


@app.on_event("startup")
def on_startup():
    """Ensures relational and analytical databases exist with golden benchmark seed."""
    from src.synthetic.loader import seed_database
    try:
        seed_database()
    except Exception as e:
        print(f"[STARTUP WARNING] Database initialization: {e}")


@app.get("/", include_in_schema=False)
def root():
    """Redirects root requests to interactive OpenAPI Swagger documentation."""
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.main:app", host=settings.API_HOST, port=settings.API_PORT, reload=settings.DEBUG)

