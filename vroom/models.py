"""ORM models for the Vroom API."""
from __future__ import annotations

from datetime import UTC, date, datetime
from decimal import Decimal

from sqlalchemy import TIMESTAMP, Date, Float, Text
from sqlalchemy.orm import Mapped, mapped_column

from vroom.db import Base


def _utcnow() -> datetime:
    """Current UTC time as a naive datetime, matching the column type."""
    return datetime.now(UTC).replace(tzinfo=None)


class Booking(Base):
    """A rental car booking."""

    __tablename__ = "booking"

    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[str] = mapped_column(Text, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    location: Mapped[str] = mapped_column(Text, nullable=False)
    car: Mapped[str] = mapped_column(Text, nullable=False)
    company_name: Mapped[str] = mapped_column(Text, nullable=False)
    company_address: Mapped[str] = mapped_column(Text, nullable=False)
    # Float(asdecimal=True) keeps the existing column type (see the Alembic
    # migration) while returning Decimal values for accurate money formatting.
    price: Mapped[Decimal] = mapped_column(
        Float(precision=2, asdecimal=True), nullable=False
    )
    created: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False), default=_utcnow, nullable=False
    )
