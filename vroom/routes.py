"""HTTP routes for the Vroom booking API.

No user authentication is required for any endpoint (a future enhancement).
Booking data is stored in the ``booking`` table.
"""
from __future__ import annotations

from flask import Blueprint, Response, jsonify, request
from pydantic import ValidationError

from vroom import service
from vroom.schemas import BookingPayload

bp = Blueprint("vroom", __name__, url_prefix="/api/vroom")

INVALID_BOOKING = "Request must contain rental car booking information"
NOT_FOUND = "Booking not found"


def _parse_payload() -> BookingPayload:
    """Validate the request body against the booking schema."""
    return BookingPayload.model_validate(request.get_json(silent=True) or {})


@bp.post("/booking")
def create_booking() -> tuple[str | Response, int]:
    try:
        payload = _parse_payload()
    except ValidationError:
        return jsonify(error=INVALID_BOOKING), 400

    return service.create_booking(payload), 201


@bp.get("/booking/<booking_id>")
def read_booking(booking_id: str) -> tuple[Response, int]:
    booking = service.read_booking(booking_id)

    if booking is None:
        return jsonify(error=NOT_FOUND), 404

    return jsonify(booking), 200


@bp.patch("/booking/<booking_id>")
def update_booking(booking_id: str) -> tuple[str | Response, int]:
    try:
        payload = _parse_payload()
    except ValidationError:
        return jsonify(error=INVALID_BOOKING), 400

    if not service.update_booking(booking_id, payload):
        return jsonify(error=NOT_FOUND), 404

    return booking_id, 200


@bp.delete("/booking/<booking_id>")
def delete_booking(booking_id: str) -> tuple[str | Response, int]:
    if not service.delete_booking(booking_id):
        return jsonify(error=NOT_FOUND), 404

    return booking_id, 200
