"""
SARAS ATLAS — Database Base & Common Model Mixins.
SQLAlchemy 2.0 Declarative Base.
"""

from datetime import datetime, timezone
import uuid
from typing import Any, Dict
from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def generate_uuid() -> str:
    """Generate a standard UUID4 hex string."""
    return str(uuid.uuid4())


def utc_now() -> datetime:
    """Current UTC timestamp."""
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    """Base declarative class for all SARAS ATLAS SQLAlchemy models."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance fields to dictionary representation."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }


class TimestampMixin:
    """Mixin adding creation and update timestamp columns."""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False
    )
