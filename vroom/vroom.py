import random
import string

from datetime import datetime
from flask import jsonify, make_response, request
from sqlalchemy.orm.exc import NoResultFound

from vroom import models


def create_booking():
    # Request should contain:
    # car <str>
    # company_address <str>
    # company_name <str>
    # end_date <str>
    # location <str>
    # price <str>
    # start_date <str>
    data = request.get_json()

    # Return error if request is missing data
    if (not data or 'car' not in data or 'company_address' not in data or
        'company_name' not in data or 'end_date' not in data or
        'location' not in data or 'price' not in data or
        'start_date' not in data):
            return make_response(
                'Request must contain rental car booking information', 400)

    # Generate random external id for booking
    external_id = ''.join(
        random.choices(string.ascii_letters + string.digits, k=16))

    # Connect to database
    session = models.Session()

    # Add booking to database
    booking = models.Booking(
        car=data['car'],
        company_address=data['company_address'],
        company_name=data['company_name'],
        end_date=datetime.strptime(data['end_date'], "%m-%d-%Y").date(),
        external_id=external_id,
        location=data['location'],
        price=float(data['price']),
        start_date=datetime.strptime(data['start_date'], "%m-%d-%Y").date()
        )

    session.add(booking)

    session.commit()

    session.close()

    return make_response(external_id, 201)


def read_booking(booking_id):
    # Connect to database
    session = models.Session()

    # Retrieve booking from database
    try:
        booking = session.query(models.Booking).with_entities(
            models.Booking.car, models.Booking.company_name,
            models.Booking.company_address, models.Booking.end_date,
            models.Booking.location, models.Booking.price,
            models.Booking.start_date).filter(
            models.Booking.external_id == booking_id).limit(1).one()

        session.close()

        booking = booking._asdict()

        booking['price'] = '%.2f' % booking['price']

        booking['start_date'] = booking['start_date'].strftime("%m-%d-%Y")
        booking['end_date'] = booking['end_date'].strftime("%m-%d-%Y")

        return jsonify(booking)

    # Return error if booking not returned from query
    except NoResultFound:
        session.close()

        return make_response('Booking not found', 404)


def update_booking(booking_id):
    # Request should contain:
    # car <str>
    # company_address <str>
    # company_name <str>
    # end_date <str>
    # location <str>
    # price <str>
    # start_date <str>
    data = request.get_json()

    # Return error if request is missing data
    if (not data or 'car' not in data or 'company_address' not in data or
        'company_name' not in data or 'end_date' not in data or
        'location' not in data or 'price' not in data or
        'start_date' not in data):
            return make_response(
                'Request must contain rental car booking information', 400)

    # Connect to database
    session = models.Session()

    # Update booking in database
    update = session.query(models.Booking).filter(
        models.Booking.external_id == booking_id).update(
        {"car": data['car'], "company_address": data['company_address'],
        "company_name": data['company_name'],
        "end_date": datetime.strptime(data['end_date'], "%m-%d-%Y").date(),
        "location": data['location'],
        "price": data['price'],
        "start_date": datetime.strptime(data['start_date'], "%m-%d-%Y").date()}
        )

    # Return error if booking not returned from query
    if update == 0:
        session.close()

        return make_response('Booking not found', 404)

    session.commit()

    session.close()

    return make_response(booking_id, 200)


def delete_booking(booking_id):
    # Connect to database
    session = models.Session()

    # Delete booking from database
    booking = session.query(models.Booking).filter(
        models.Booking.external_id == booking_id).delete()

    # Return error if booking not returned from query
    if booking == 0:
        session.close()

        return make_response('Booking not found', 404)

    session.commit()

    session.close()

    return make_response(booking_id, 200)
