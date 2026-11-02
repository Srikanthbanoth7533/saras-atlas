"""
SARAS ATLAS — Database Session & Engine Configuration.
Implements SQLite WAL mode with strict foreign key integrity (ADR-001)
and provides embedded DuckDB connection factories.
"""

from contextlib import contextmanager
from typing import Generator
import duckdb
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from src.config import settings
from src.database.base import Base


# Create SQLAlchemy 2.0 Engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)


# SQLite PRAGMA configuration for high concurrency, durability, and foreign key integrity
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Enforce WAL mode and foreign key constraints on SQLite connections."""
    if "sqlite" in settings.DATABASE_URL:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA synchronous=NORMAL;")
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Context manager for transactional database sessions."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency for injecting database sessions."""
    with get_db_session() as session:
        yield session


def init_db() -> None:
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)


def drop_db() -> None:
    """Drop all tables in the database (used in testing)."""
    Base.metadata.drop_all(bind=engine)


def get_duckdb_connection(read_only: bool = False) -> duckdb.DuckDBPyConnection:
    """
    Returns an embedded DuckDB connection for analytical OLAP queries.
    """
    return duckdb.connect(settings.DUCKDB_PATH, read_only=read_only)

