"""
SARAS ATLAS — Configuration Module
Uses pydantic-settings to manage environment settings, database paths, and solver bounds.
"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application and environment configuration settings."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    APP_NAME: str = "SARAS ATLAS"
    APP_VERSION: str = "1.0.0"
    ENV: str = "development"
    DEBUG: bool = False

    # Base Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "data"

    # Database Configuration (In-Process Hybrid: SQLite WAL + DuckDB)
    DATABASE_URL: str = f"sqlite:///{(DATA_DIR / 'saras_atlas.db').as_posix()}"
    DUCKDB_PATH: str = f"{(DATA_DIR / 'saras_atlas_analytics.duckdb').as_posix()}"

    # Simulation & Optimization Solver Bounds
    DEFAULT_HORIZON_DAYS: int = 90
    SYNTHETIC_SEED: int = 42
    MAX_SOLVER_TIME_SECONDS: float = 3.0
    TWO_MAN_RULE_THRESHOLD_DOLLARS: float = 25000.0

    # API Network Binding (Strict Localhost)
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000

    def ensure_directories(self) -> None:
        """Ensure necessary runtime directories exist on the filesystem."""
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)


settings = Settings()
settings.ensure_directories()

