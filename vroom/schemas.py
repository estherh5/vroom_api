"""Request and response schemas for the Vroom API."""
from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_serializer, field_validator

DATE_FORMAT = "%m-%d-%Y"


class BookingPayload(BaseModel):
    """Validated booking data sent by clients on POST and PATCH."""

    model_config = ConfigDict(extra="ignore")

    car: str
    company_address: str
    company_name: str
    location: str
    price: Decimal
    start_date: date
    end_date: date

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def _parse_date(cls, value: object) -> object:
        if isinstance(value, str):
            return datetime.strptime(value, DATE_FORMAT).date()
        return value


class BookingResponse(BaseModel):
    """Booking data returned to clients, formatted to match the legacy API."""

    model_config = ConfigDict(from_attributes=True)

    car: str
    company_address: str
    company_name: str
    end_date: date
    location: str
    price: Decimal
    start_date: date

    @field_serializer("start_date", "end_date")
    def _serialize_date(self, value: date) -> str:
        return value.strftime(DATE_FORMAT)

    @field_serializer("price")
    def _serialize_price(self, value: Decimal) -> str:
        return f"{value:.2f}"
