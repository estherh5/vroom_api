import os

from flask import Flask, request
from flask_cors import CORS

from vroom import vroom

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
if os.environ['ENV_TYPE'] == 'Dev':
    app.config['DEBUG'] = True


@app.route('/api/vroom/booking', methods=['POST'])
def vroom_booking():
    # Post Vroom booking data when client sends the jsonified booking
    # information in the request body; no bearer token needed for user
    # authentication
    if request.method == 'POST':
        return vroom.create_booking()


@app.route('/api/vroom/booking/<booking_id>', methods=['GET', 'PATCH',
    'DELETE'])
def vroom_booking_id(booking_id):
    # Get Vroom booking data when client sends the booking id in the request
    # URL; no bearer token needed for user authentication
    if request.method == 'GET':
        return vroom.read_booking(booking_id)

    # Update Vroom booking data when client sends the booking id in the request
    # URL and the jsonified updated booking information in the request body; no
    # bearer token needed for user authentication
    if request.method == 'PATCH':
        return vroom.update_booking(booking_id)

    # Delete Vroom booking data when client sends the booking id in the request
    # URL; no bearer token needed for user authentication
    if request.method == 'DELETE':
        return vroom.delete_booking(booking_id)
