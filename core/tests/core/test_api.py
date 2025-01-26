import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from core import create_app
from utils.commands import CommandType

class TestApi(unittest.TestCase):
    def setUp(self):
        app: Flask = create_app()
        app.config.update({
            "TESTING": True
        })

        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()

    @patch("core.api.OllamaService.send_prompt")
    @patch("core.api.PerplexicaService.query_internet")
    @patch("core.api.OllamaService.get_command_from_prompt")
    def test_handle_prompt_valid_web_search_prompt(self, mock_get_command, mock_query_internet, mock_send_prompt):
        # arrange
        mock_command = MagicMock()
        mock_command.command_type = CommandType.WEB_SEARCH
        mock_command.parameters = []
        mock_get_command.return_value = mock_command
        mock_query_internet.return_value = (200, '{"perplexica_response":"Six legs"}')

        prompt_response = "Ants have six legs"
        mock_send_prompt.return_value = prompt_response

        prompt = "How many legs do ants have?"
        path = f"/api/handle-prompt?p={prompt}"

        # act
        response = self.client.get(path)

        # assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data,  prompt_response.encode('ASCII'))

    def test_handle_prompt_no_prompt(self):
        # arrange
        path = f"/api/handle-prompt"

        # act
        response = self.client.get(path)

        # assert
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"error", response.data)

    def test_handle_prompt_too_short_prompt(self):
        # arrange
        prompt = "ab"
        path = f"/api/handle-prompt?p={prompt}"

        # act
        response = self.client.get(path)

        # assert
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"error", response.data)
