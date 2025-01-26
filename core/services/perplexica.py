import requests
from typing import Tuple, Dict, Optional, Any
from enum import Enum

class FocusModeEnum(Enum):
    WEB_SEARCH = "webSearch"
    ACADEMIC_SEARCH = "academicSearch"
    WRITING_ASSISTANT = "writingAssistant"
    WOLFRAM_ALPHA_SEARCH = "wolframAlphaSearch"
    YOUTUBE_SEARCH = "youtubeSearch"
    REDDIT_SEARCH = "redditSearch"

class PerplexicaService:
    @classmethod
    def query_internet(cls, query: str, model: str = "llama3:latest",
                       focus_mode: FocusModeEnum = FocusModeEnum.WEB_SEARCH
                       ) -> Tuple[int, Optional[Dict[str, Any]]]:
        if len(query) < 3:
            return 400, { "error": "Query can't be less than 3 characters long" }

        body = {
            "chatModel": {
                "provider": "ollama",
                "model": model
            },

            #"embeddingModel": {
            #    "provider": "openai",
            #    "model": "text-embedding-3-large"
            #},

            "focusMode": focus_mode.value,
            "query": query,

            #"history": [
            #    ["human", "Hi, how are you?"],
            #    ["assistant", "I am doing well, how can I help you today?"]
            #]
        }

        px_response = requests.post("http://localhost:1101/api/search", json = body)
        print(f"Perplexica response status: {px_response.status_code}")

        if not px_response.ok:
            error_message = px_response.json()["message"]
            print(error_message)
            return px_response.status_code, { "error": error_message }

        return px_response.status_code, px_response.json()
