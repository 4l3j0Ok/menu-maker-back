from pydantic import BaseModel
from typing import Union


class Response(BaseModel):
    success: bool
    payload: Union[dict, list, None]
    message: Union[str, None]
