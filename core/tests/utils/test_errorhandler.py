import unittest
import utils.errorhandler as errorhandler
from core import create_app # this works even if the LSP complains about it

class TestErrorhandler(unittest.TestCase):

    # automatically called by unittest before tests
    def setUp(self) -> None:
        app = create_app()
        app.config.update({
            "TESTING": True
        })

        self.app = app
        self.client = app.test_client()

        # app.testing = True
        # self.app_context = app.app_context()
        # self.app_context.push()

    # def tearDown(self) -> None:
        # self.app_context.pop()

    def test_check_service_error_valid_data(self):
        data = {
            "something": 5,
            "another": ("test", {}, ''),
            "string": None
        }

        status_code = 200
        is_error = errorhandler.check_service_error(data, status_code)

        self.assertFalse(is_error, "Data should be valid with status 200")

    def test_get_service_error_response_valid_error(self):
        data = {
            "error": "This is a valid error"
        }

        status_code = 400
        is_error = errorhandler.check_service_error(data, status_code)

        self.assertTrue(is_error)

        with self.app.app_context():
            err_response = errorhandler.get_service_error_response(data, status_code)

        self.assertEqual(err_response.data, b'{"error":"This is a valid error"}\n', "Error message should be found")
        self.assertIs(err_response.status_code, status_code, "Error status code should match")

    def test_get_service_error_response_missing_error(self):
        data = {
            "message": "This is my bad error message"
        }

        status_code = 400
        is_error = errorhandler.check_service_error(data, status_code)

        self.assertTrue(is_error)

        with self.app.app_context():
            err_response = errorhandler.get_service_error_response(data, status_code)

        self.assertEqual(err_response.data, b'{"error":"Something went wrong. Data might be malformatted."}\n', "Should get generic error response")
        self.assertIs(err_response.status_code, status_code, "Error status code should match")
