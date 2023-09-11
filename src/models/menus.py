from pydantic import BaseModel
from bson import ObjectId


class Menu(BaseModel):
    name: str
    description: str


class MenuDB(Menu):
    id: str
    sections: list[str]

    def __init__(self, **menu):
        if "_id" in menu and isinstance(menu["_id"], ObjectId):
            menu["id"] = str(menu["_id"])
        super().__init__(**menu)
