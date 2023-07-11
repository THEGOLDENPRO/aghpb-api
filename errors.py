from pydantic import BaseModel

class APIException(Exception):
    def __init__(self, msg) -> None:
        self.msg = msg
        super().__init__(msg)


class APIError(BaseModel):
    error: str
    message: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "CategoryNotFound",
                    "description": "The category 'rust' was not found!"
                }
            ]
        }
    }