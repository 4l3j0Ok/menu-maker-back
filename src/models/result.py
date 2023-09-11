from typing import Union
from pydantic import BaseModel


class Result(BaseModel):
    payload: Union[dict, list, None] = None
    message: Union[str, None] = None
