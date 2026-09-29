"""Tests for the /api/vroom/booking endpoints [POST, GET, PATCH, DELETE]."""
from __future__ import annotations

from flask.testing import FlaskClient

BOOKING = {
    "car": "ECAR",
    "company_address": "6975 Norwitch Drive, Philadelphia, PA",
    "company_name": "Payless",
    "end_date": "09-21-2018",
    "location": "Philadelphia, PA, USA",
    "price": "41.68",
    "start_date": "09-21-2018",
}

UPDATED_BOOKING = {
    "car": "LDAR",
    "company_address": "7500 Holstein Ave, Philadelphia, PA",
    "company_name": "Thrifty",
    "end_date": "10-01-2018",
    "location": "Philadelphia, PA, USA",
    "price": "219.00",
    "start_date": "09-30-2018",
}

INVALID_BOOKING = {"error": "Request must contain rental car booking information"}
NOT_FOUND = {"error": "Booking not found"}


def test_booking_post_get_patch_delete(client: FlaskClient) -> None:
    # POST
    post_response = client.post("/api/vroom/booking", json=BOOKING)
    booking_id = post_response.get_data(as_text=True)
    assert post_response.status_code == 201

    # GET
    get_response = client.get(f"/api/vroom/booking/{booking_id}")
    assert get_response.status_code == 200
    assert get_response.get_json() == BOOKING

    # PATCH
    patch_response = client.patch(
        f"/api/vroom/booking/{booking_id}", json=UPDATED_BOOKING
    )
    patch_get_response = client.get(f"/api/vroom/booking/{booking_id}")
    assert patch_response.status_code == 200
    assert patch_get_response.status_code == 200
    assert patch_get_response.get_json() == UPDATED_BOOKING

    # DELETE
    delete_response = client.delete(f"/api/vroom/booking/{booking_id}")
    delete_get_response = client.get(f"/api/vroom/booking/{booking_id}")
    assert delete_response.status_code == 200
    assert delete_get_response.status_code == 404
    assert delete_get_response.get_json() == NOT_FOUND


def test_booking_post_data_error(client: FlaskClient) -> None:
    response = client.post("/api/vroom/booking")
    assert response.status_code == 400
    assert response.get_json() == INVALID_BOOKING


def test_booking_patch_data_error(client: FlaskClient) -> None:
    response = client.patch("/api/vroom/booking/test")
    assert response.status_code == 400
    assert response.get_json() == INVALID_BOOKING


def test_booking_patch_not_found(client: FlaskClient) -> None:
    response = client.patch("/api/vroom/booking/test", json=UPDATED_BOOKING)
    assert response.status_code == 404
    assert response.get_json() == NOT_FOUND


def test_booking_delete_not_found(client: FlaskClient) -> None:
    response = client.delete("/api/vroom/booking/test")
    assert response.status_code == 404
    assert response.get_json() == NOT_FOUND


def test_oversized_body_is_rejected(client: FlaskClient) -> None:
    response = client.post(
        "/api/vroom/booking",
        data="x" * (16 * 1024 + 1),
        content_type="application/json",
    )
    assert response.status_code == 413


def test_cors_allows_only_the_vroom_frontend(client: FlaskClient) -> None:
    allowed = client.get(
        "/api/vroom/booking/x", headers={"Origin": "https://vroom.crystalprism.io"}
    )
    assert (
        allowed.headers.get("Access-Control-Allow-Origin")
        == "https://vroom.crystalprism.io"
    )

    other = client.get(
        "/api/vroom/booking/x", headers={"Origin": "https://evil.example"}
    )
    assert "Access-Control-Allow-Origin" not in other.headers
