from flask import Blueprint, make_response, request, abort
import datetime
from typing import Optional, Dict, Any
import utils.errorhandler as errorhandler
from utils.commands import CommandType
from services.weather import WeatherService
from services.perplexica import PerplexicaService
from services.ollama import OllamaService

bp = Blueprint("api", __name__, url_prefix="/api")

@bp.route("/")
def api_index():
    return "API usage instructions here"

@bp.route("/services/")
def service_index():
    return "API service usage instructions here"

@bp.route("/services/perplexica/")
def perplexica_service_index():
    query = request.args.get("q")

    if query is None or len(query) < 3:
        response = make_response({"error":"Query is empty or too short"})
        response.status_code = 400
        return response

    status_code, data = PerplexicaService.query_internet(query)

    if errorhandler.check_service_error(data, status_code):
        return errorhandler.get_service_error_response(data, status_code)

    if data is None:
        abort(status_code)

    return data

@bp.route("/services/weather/")
def weather_service_index():
    city = request.args.get("city", "Helsinki")
    status_code, data = WeatherService.get_current_weather(city)

    if errorhandler.check_service_error(data, status_code):
        return errorhandler.get_service_error_response(data, status_code)

    if data is None:
        abort(status_code)

    return data

@bp.route("/services/music/")
def music_service_index():
    query = request.args.get("query", "")
    return f"<p>This is the music service. Try spotube?</p><p>You queried: {query}</p>"

@bp.route("/handle-prompt")
def handle_prompt():
    prompt = request.args.get("p", None)

    if prompt is None or len(prompt) < 3:
        response = make_response({"error":"Prompt is empty or too short"})
        response.status_code = 400
        return response

    command = OllamaService.get_command_from_prompt(prompt)

    if command is None:
        response = make_response({ "error": "Prompt didn't match a command" })
        response.status_code = 400
        return response

    data: Optional[Dict[str, Any]] = None
    status_code = 500

    match command.command_type:
        case CommandType.WEATHER_CURRENT:
            print("Handling current weather command...")
            status_code, data = WeatherService.get_current_weather("Helsinki")

        case CommandType.WEATHER_FORECAST:
            print("Handling weather forecast command...")

            days = 1
            match command.parameters[0]:
                case 'tomorrow':
                    days = 2

            status_code, data = WeatherService.get_weather_forecast("Helsinki", days)

        case CommandType.WEB_SEARCH:
            print("Handling web search command...")

            status_code, data = PerplexicaService.query_internet(prompt)

    if errorhandler.check_service_error(data, status_code):
        return errorhandler.get_service_error_response(data, status_code)

    if data is None:
        abort(status_code)

    summary_prompt = (f"Give a short one sentence answer to the user prompt '{prompt}' "
                      f"based on this data: '{data} Current time: {datetime.datetime.now()}'. "
                      "Answer with one short sentence that includes relevant details that a human might want to know.")

    return OllamaService.send_prompt(summary_prompt)
