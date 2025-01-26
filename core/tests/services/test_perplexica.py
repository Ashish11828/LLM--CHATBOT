from services.perplexica import PerplexicaService, FocusModeEnum
import unittest
from unittest.mock import patch, MagicMock
from core import create_app

class TestPerplexica(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config.update({
            "TESTING": True
        })

        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch("services.perplexica.requests.post")
    def test_query_internet_valid_simple_query(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.json.return_value = { "perplexica_response": "valid query" }
        mock_post.return_value = mock_response

        # query_internet uses requests.post to hit perplexica, so we use a mock
        # method instead with a mock response
        status_code, response_json = PerplexicaService.query_internet("How many legs do ants have?")

        self.assertEqual(status_code, 200, "Should be 200")
        self.assertIsNotNone(response_json, "Response json exists")
        assert response_json is not None
        self.assertGreater(len(response_json.keys()), 0, "Response has content")

    @patch("services.perplexica.requests.post")
    def test_query_internet_valid_custom_query(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.json.return_value = { "perplexica_response": "valid query" }
        mock_post.return_value = mock_response

        query = "How many legs do ants have?"
        model = "llama3:latest"
        focus_mode = FocusModeEnum.WEB_SEARCH
        status_code, response_json = PerplexicaService.query_internet(query, model, focus_mode)

        self.assertEqual(status_code, 200, "Should be 200")
        self.assertIsNotNone(response_json, "Response json should exist")
        assert response_json is not None
        self.assertGreater(len(response_json.keys()), 0, "Response has content")

    def test_query_internet_invalid_simple_query(self):
        # query_internet fails early so the Perplexica request is never sent
        status_code, response_json = PerplexicaService.query_internet("a")

        self.assertEqual(status_code, 400, "Should be bad request code")
        self.assertIsNotNone(response_json, "Response json should exist")
        assert response_json is not None
        self.assertIn("error", response_json.keys(), "error key should be in response json")


    def test_query_internet_invalid_custom_query(self):
        query = "b"
        model = "llama3:latest"
        focus_mode = FocusModeEnum.WEB_SEARCH
        status_code, response_json = PerplexicaService.query_internet(query, model, focus_mode)

        self.assertEqual(status_code, 400, "Should be bad request code")
        self.assertIsNotNone(response_json, "Response json should exist")
        assert response_json is not None
        self.assertIn("error", response_json.keys(), "error key should be in response json")

    @patch("services.perplexica.requests.post")
    def test_query_internet_invalid_model(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.ok = False
        mock_response.json.return_value = { "message": "perplexica error message" }
        mock_post.return_value = mock_response

        query = "How many legs do ants have?"
        model = "llma38:latst"
        focus_mode = FocusModeEnum.WEB_SEARCH
        status_code, response_json = PerplexicaService.query_internet(query, model, focus_mode)

        self.assertEqual(status_code, 400, "Should be 400")
        self.assertIsNotNone(response_json, "Response json should exist")
        assert response_json is not None
        self.assertIn("error", response_json.keys(), "error key should be in response json")
        self.assertGreater(len(response_json["error"]), 0, "error message has content")
