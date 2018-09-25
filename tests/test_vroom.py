import json

from utils.tests import VroomTestCase


# Test /api/vroom/booking endpoint [POST, GET, PATCH, DELETE]
class TestBooking(VroomTestCase):
    def test_booking_post_get_patch_delete(self):
        # Arrange [POST]
        booking = {
            'car': 'ECAR',
            'company_address': '6975 Norwitch Drive, Philadelphia, PA',
            'company_name': 'Payless',
            'end_date': '09-21-2018',
            'location': 'Philadelphia, PA, USA',
            'price': '41.68',
            'start_date': '09-21-2018'
        }

        # Act [POST]
        post_response = self.client.post(
            '/api/vroom/booking',
            data=json.dumps(booking),
            content_type='application/json'
            )
        booking_id = post_response.get_data(as_text=True)

        # Assert [POST]
        self.assertEqual(post_response.status_code, 201)

        # Act [GET]
        get_response = self.client.get(
            '/api/vroom/booking/' + booking_id
            )
        booking_response = json.loads(get_response.get_data(as_text=True))

        # Assert [GET]
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(booking_response, booking)

        # Arrange [PATCH]
        updated_booking = {
            'car': 'LDAR',
            'company_address': '7500 Holstein Ave, Philadelphia, PA',
            'company_name': 'Thrifty',
            'end_date': '10-01-2018',
            'location': 'Philadelphia, PA, USA',
            'price': '219.00',
            'start_date': '09-30-2018'
        }

        # Act [PATCH]
        patch_response = self.client.patch(
            '/api/vroom/booking/' + booking_id,
            data=json.dumps(updated_booking),
            content_type='application/json'
            )

        patch_get_response = self.client.get(
            '/api/vroom/booking/' + booking_id
            )
        updated_booking_response = json.loads(
            patch_get_response.get_data(as_text=True))

        # Assert [PATCH]
        self.assertEqual(patch_response.status_code, 200)
        self.assertEqual(patch_get_response.status_code, 200)
        self.assertEqual(updated_booking_response, updated_booking)

        # Act [DELETE]
        delete_response = self.client.delete(
            '/api/vroom/booking/' + booking_id
            )

        delete_get_response = self.client.get(
            '/api/vroom/booking/' + booking_id
            )
        error = delete_get_response.get_data(as_text=True)

        # Assert [DELETE]
        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(delete_get_response.status_code, 404)
        self.assertEqual(error, 'Booking not found')

    def test_booking_post_data_error(self):
        # Act
        post_response = self.client.post(
            '/api/vroom/booking'
            )
        error = post_response.get_data(as_text=True)

        # Assert
        self.assertEqual(post_response.status_code, 400)
        self.assertEqual(
            error, 'Request must contain rental car booking information')

    def test_booking_patch_data_error(self):
        # Arrange
        booking_id = 'test'

        # Act
        patch_response = self.client.patch(
            '/api/vroom/booking/' + booking_id
            )
        error = patch_response.get_data(as_text=True)

        # Assert
        self.assertEqual(patch_response.status_code, 400)
        self.assertEqual(
            error, 'Request must contain rental car booking information')

    def test_booking_patch_not_found(self):
        # Arrange
        booking_id = 'test'
        updated_booking = {
            'car': 'LDAR',
            'company_address': '7500 Holstein Ave, Philadelphia, PA',
            'company_name': 'Thrifty',
            'end_date': '10-01-2018',
            'location': 'Philadelphia, PA, USA',
            'price': '219.00',
            'start_date': '09-30-2018'
        }

        # Act [PATCH]
        patch_response = self.client.patch(
            '/api/vroom/booking/' + booking_id,
            data=json.dumps(updated_booking),
            content_type='application/json'
            )
        error = patch_response.get_data(as_text=True)

        # Assert
        self.assertEqual(patch_response.status_code, 404)
        self.assertEqual(error, 'Booking not found')

    def test_booking_delete_not_found(self):
        # Arrange
        booking_id = 'test'

        # Act
        delete_response = self.client.delete(
            '/api/vroom/booking/' + booking_id
            )
        error = delete_response.get_data(as_text=True)

        # Assert
        self.assertEqual(delete_response.status_code, 404)
        self.assertEqual(error, 'Booking not found')
