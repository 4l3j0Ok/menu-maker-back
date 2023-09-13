from pydantic import BaseModel
from bson import ObjectId
from typing import Union


class Menu(BaseModel):
    name: str
    description: str
    sections: Union[None, list[str]] = None


class MenuDB(Menu):
    id: str

    def __init__(self, **menu):
        if "_id" in menu and isinstance(menu["_id"], ObjectId):
            menu["id"] = str(menu["_id"])
        super().__init__(**menu)
