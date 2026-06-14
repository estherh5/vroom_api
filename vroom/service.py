"""Business logic for creating and managing Vroom bookings."""
from __future__ import annotations

import secrets
from typing import Any

from sqlalchemy import select

from vroom.db import Session
from vroom.models import Booking
from vroom.schemas import BookingPayload, BookingResponse


def create_booking(payload: BookingPayload) -> str:
    """Persist a new booking and return its external confirmation code."""
    external_id = secrets.token_urlsafe(12)

    with Session.begin() as session:
        session.add(
            Booking(
                external_id=external_id,
                car=payload.car,
                company_address=payload.company_address,
                company_name=payload.company_name,
                location=payload.location,
                price=payload.price,
                start_date=payload.start_date,
                end_date=payload.end_date,
            )
        )

    return external_id


def read_booking(booking_id: str) -> dict[str, Any] | None:
    """Return the booking with the given external id, or None if absent."""
    with Session() as session:
        booking = session.scalars(
            select(Booking).where(Booking.external_id == booking_id)
        ).first()

        if booking is None:
            return None

        return BookingResponse.model_validate(booking).model_dump()


def update_booking(booking_id: str, payload: BookingPayload) -> bool:
    """Update an existing booking. Returns False if it does not exist."""
    with Session.begin() as session:
        booking = session.scalars(
            select(Booking).where(Booking.external_id == booking_id)
        ).first()

        if booking is None:
            return False

        booking.car = payload.car
        booking.company_address = payload.company_address
        booking.company_name = payload.company_name
        booking.location = payload.location
        booking.price = payload.price
        booking.start_date = payload.start_date
        booking.end_date = payload.end_date

    return True


def delete_booking(booking_id: str) -> bool:
    """Delete a booking. Returns False if it does not exist."""
    with Session.begin() as session:
        booking = session.scalars(
            select(Booking).where(Booking.external_id == booking_id)
        ).first()

        if booking is None:
            return False

        session.delete(booking)

    return True
