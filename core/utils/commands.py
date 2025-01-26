from enum import Enum
from dataclasses import dataclass
from typing import Any, List

class CommandType(Enum):
    WEATHER_CURRENT = 1
    WEATHER_FORECAST = 2
    WEB_SEARCH = 3

@dataclass
class Command:
    command_type: CommandType
    parameters: List[Any]
