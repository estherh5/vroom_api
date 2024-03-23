[![Build Status](https://travis-ci.com/estherh5/vroom_api.svg?branch=master)](https://travis-ci.com/estherh5/vroom_api)
[![codecov](https://codecov.io/gh/estherh5/vroom_api/branch/master/graph/badge.svg)](https://codecov.io/gh/estherh5/vroom_api)

# Vroom
[Vroom](https://vroom.crystalprism.io) is a [React](https://reactjs.org/) web app that makes renting a car quick and easy. Vroom displays an interactive portal where you can search for a location and dates/times to pick up and drop off your rental car, then select a rental car from different rental companies, and lastly confirm your booking and see a map of how to get to your intended pick-up location. Vroom uses [React Geosuggest](https://github.com/ubilabs/react-geosuggest) to suggest Google Maps locations as you search for your pick-up and drop-off cities, as well as [Airbnb's react-dates](https://github.com/airbnb/react-dates) to provide a calendar-based date range selector. Car rental data is acquired via [RapidAPI's Car Rental API](https://rapidapi.com/DataCrawler/api/booking-com15). When you confirm your booking, your information gets sent to a RESTful API that stores your data in a PostgreSQL database and returns a unique confirmation code for your booking.

## Setup
1. Clone this repository locally or on your server (`git clone https://github.com/estherh5/vroom_api`).
2. Enter the `vroom_api` directory, and install requirements by running `pip install -r requirements.txt`.
3. Create a PostgreSQL database to store Vroom booking data, as well as a user that has all privileges on your database.
4. Set the following environment variables for the API:
    * `FLASK_APP` for the Flask application name for your server ("server.py")
    * `ENV_TYPE` for the environment status (set this to "Dev" for testing or "Prod" for live)
    * `VIRTUAL_ENV_NAME` for the name of your virtual environment (e.g., `vroom`); this is used to schedule automatic database backups with crontab
    * `PATH` for the path to the executable files that will run when automatic database backups are performed via crontab; you should append the path to your PostgreSQL directory here (e.g., `$PATH:/Applications/Postgres.app/Contents/Versions/latest/bin`)
    * `DB_CONNECTION` for the [database URL](http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls) to connect to your database via SQLAlchemy ORM (i.e., '<dialect+driver://username:password@host:port/database>')
    * `DB_NAME` for the name of your database
    * `DB_USER` for the user who has all privileges on your database
    * [`AWS_ACCESS_KEY_ID`](http://boto3.readthedocs.io/en/latest/guide/configuration.html#environment-variables) for the access key for your AWS account stored on Amazon S3 buckets
    * [`AWS_SECRET_ACCESS_KEY`](http://boto3.readthedocs.io/en/latest/guide/configuration.html#environment-variables) for the secret key for your AWS account stored on Amazon S3 buckets
    * `S3_BUCKET` for the name of your S3 bucket, which should not contain any periods (e.g., `crystalprism`)
    * `S3_BACKUP_DIR` for the name of the S3 bucket's folder for database backups (e.g., `vroom-db-backups/`)
    * `BACKUP_DIR` for the directory where your database backups are stored locally
5. Load the initial database structure by running `alembic upgrade head`.
    * Note that you might need to add `PYTHONPATH=.` to the beginning of your revision command if Alembic can't find your module.
6. Set up weekly backups for the database by running `python management.py sched_backup`.
7. Start the server by running `flask run` (if you are making changes while the server is running, enter `flask run --reload` instead for instant updates).

## API
To post and retrieve data for Vroom bookings, a client can send a request to the following endpoints. Booking data gets saved in the database table "booking":
<p align="center"><img title="Vroom Database" src ="images/vroom-database.png" /></p>

\
**POST** /api/vroom/booking
* Post booking data by sending the jsonified booking information in the request body. No bearer token is needed in the request Authorization header (in the future, user authentication will be required).
* Example request body:
```javascript
{
    "car": "ECAR",
    "company_address": "6975 Norwitch Drive, Philadelphia, PA",
    "company_name": "Payless",
    "end_date": "09-21-2018",
    "location": "Philadelphia, PA, USA",
    "price": "41.68",
    "start_date": "09-21-2018"
}
```

\
**GET** /api/vroom/booking/[booking_id]
* Retrieve booking data by sending the booking id in the request URL. No bearer token is needed in the request Authorization header (in the future, user authentication will be required).
* Example response body:
```javascript
{
    "car": "LDAR",
    "company_address": "7500 Holstein Ave, Philadelphia, PA",
    "company_name": "Thrifty",
    "end_date": "10-01-2018",
    "location": "Philadelphia, PA, USA",
    "price": "219.00",
    "start_date": "09-30-2018"
}
```

\
**PATCH** /api/vroom/booking/[booking_id]
* Update booking data by sending the booking id in the request URL and the updated booking information in the request body. No bearer token is needed in the request Authorization header (in the future, user authentication will be required).
* Example request body:
```javascript
{
    "car": "CCAR",
    "company_address": "6975 Norwitch Drive, Philadelphia, PA",
    "company_name": "Payless",
    "end_date":" 09-30-2018",
    "location": "Philadelphia, PA, USA",
    "price": "94.54",
    "start_date": "09-29-2018"
}
```

\
**DELETE** /api/vroom/booking/[booking_id]
* Delete booking data by sending the booking id in the request URL. No bearer token is needed in the request Authorization header (in the future, user authentication will be required).
* Example response body:
```javascript
<booking_id>
```
