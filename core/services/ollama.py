from typing import Optional
import requests
import json
from utils.commands import Command, CommandType

class OllamaService:
    __PROMPT_URL = "http://localhost:11434/api/generate"
    __DEFAULT_MODEL = "llama3:latest"

    @classmethod
    def send_prompt(cls, prompt: str) -> str:
        body = {
            "model": cls.__DEFAULT_MODEL,
            "stream": False,
            "prompt": prompt
        }

        response = requests.post(cls.__PROMPT_URL, json = body)
        response_json = response.json()
        return response_json["response"]

    @classmethod
    def get_command_from_prompt(cls, prompt: str) -> Optional[Command]:
        if len(prompt) < 3:
            return None

        commands_string = ""

        for command in CommandType:
            commands_string += f"{command.value}. {command.name}; "

        prompt_string = (f"Answer only with a number and a parameter list. Which of the given commands is the best "
                         f"match to the given prompt and what are the parameters? The prompt might not directly reference a command. "
                         f"If none seem to match, resort to web search with an empty parameter list. "
                         f"Commands: {commands_string}Example prompt: Will it rain today? Matching "
                         f"response: {CommandType.WEATHER_FORECAST.value}, [\"today\"]. Example prompt: How many legs "
                         f"do ants have? Matching response: {CommandType.WEB_SEARCH.value}, []. Example prompt: "
                         f"Is it cold tomorrow? Matching response: {CommandType.WEATHER_FORECAST.value}, [\"tomorrow\"]. "
                         f"Example prompt: what's the temperature. Matching response: {CommandType.WEATHER_CURRENT.value}, [] "
                         f"Example prompt: Nothing really matters. Resort to web search: "
                         f"{CommandType.WEB_SEARCH.value}, []. Your turn. Prompt: {prompt}")

        response_string: str = cls.send_prompt(prompt_string)
        command_args = response_string.split(', ')
        command_number = int(command_args[0])
        command_parameters = json.loads(command_args[1])
        # print(f"command: {command_number} ({type(command_number)}), params: {command_parameters} ({type(command_parameters)})")

        if command_number == 0 or command_number > len(CommandType):
            return None

        command_type = None
        
        for command in CommandType:
            if command.value == command_number:
                command_type = command

        if command_type is None:
            # print("command type: None")
            return None

        # print(f"command type: {command_type.name}")

        return Command(command_type=command_type, parameters=command_parameters)
