from pydantic import BaseModel
from typing_extensions import TypedDict


class Detail(TypedDict):
    payload: dict | list | None
    message: str | None


class Success(BaseModel):
    detail: Detail


class Failed(BaseModel):
    detail: Detail


class Result(BaseModel):
    success: list[Success] | list
    failed: list[Failed] | list