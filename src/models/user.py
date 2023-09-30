from pydantic import BaseModel
from typing import TypedDict
from bson import ObjectId


class User(BaseModel):
    username: str
    name: str
    email: str


class UserDB(User):
    id: str | None
    password: str

    def __init__(self, **user):
        if "_id" in user and isinstance(user["_id"], ObjectId):
            user["id"] = str(user["_id"])
        super().__init__(**user)

