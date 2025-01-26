from typing import Any, Dict, Optional
from flask import Response, make_response

def check_service_error(data: Optional[Dict[str, Any]], status_code: int):
    if data is None or (status_code >= 400 and status_code <= 600):
        print("Error!")
        return True

    return False

def get_service_error_response(data: Optional[Dict[str, Any]], status_code: int) -> Response:
    if data is not None:
        error = data.get("error")

        if error is not None:
            response = make_response({ "error": error })
            response.status_code = status_code
            return response
        else:
            print("No error key in data dictionary")
    else:
        print("Data is empty")

    response = make_response({ "error": "Something went wrong. Data might be malformatted." })
    response.status_code = status_code
    return response
