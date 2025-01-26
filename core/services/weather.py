import os
import requests
from typing import Tuple, Dict, Optional, Any

class WeatherService:
    __API_KEY = os.getenv("WEATHERAPI_COM_APIKEY")
    __API_BASE_URL = "http://api.weatherapi.com/v1"

    @classmethod
    def __get_weather(cls, url: str, parameters: Dict[str, Any]):
        api_response: requests.Response = requests.get(url = cls.__API_BASE_URL + url, params = parameters)

        if not api_response.ok:
            return api_response.status_code, {"error":"Server error"}

        json_data: Dict = api_response.json()

        return api_response.status_code, json_data

    @classmethod
    def get_current_weather(cls, city: str) -> Tuple[int, Optional[Dict[str, Any]]]:
        if len(city) < 3:
            return 400, {"error":"Invalid city"}

        if (cls.__API_KEY is None):
            return 500, {"error":"Server error"}

        parameters = { "key": cls.__API_KEY, "q": city }
        return cls.__get_weather("/current.json", parameters)

    @classmethod
    def get_weather_forecast(cls, city: str, days: int = 1) -> Tuple[int, Optional[Dict[str, Any]]]:
        if (cls.__API_KEY is None):
            return 500, {"error":"Server error"}

        parameters = { "key": cls.__API_KEY, "q": city, "days": days }
        return cls.__get_weather("/forecast.json", parameters)
