"""
SARAS ATLAS — Enterprise REST API.
Commerce Resilience & Decision Simulation Platform.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.config import settings
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
)

app = FastAPI(
    title="SARAS ATLAS API",
    description=(
        "Enterprise Digital Twin & Decision Simulation Platform for E-Commerce and Retail. "
        "Provides multi-echelon network topology, operational risk detection, 90-day discrete "
        "difference scenario simulation, Google OR-Tools MILP prescriptive optimization, "
        "and Two-Man Rule governance with SHA-256 cryptographic audit trails."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Enable CORS for local and web UI clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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


@app.get("/", include_in_schema=False)
def root():
    """Redirects root requests to interactive OpenAPI Swagger documentation."""
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.main:app", host=settings.API_HOST, port=settings.API_PORT, reload=settings.DEBUG)

