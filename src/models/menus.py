from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Union


class Menu(BaseModel):
    name: str = Field(example="Clock")
    description: str = Field(example="El menú de Clock, tu restaurante favorito.")
    sections: Union[list[str], None] = Field(example=["507f1f77bcf86cd799439011", "00000020f51bb4362eee2a4d"])
    img: Union[str, None] = Field(example="https://example.com/")


class MenuDB(Menu):
    id: str

    def __init__(self, **menu):
        if "_id" in menu and isinstance(menu["_id"], ObjectId):
            menu["id"] = str(menu["_id"])
        if "sections" in menu:
            menu["sections"] = [str(section) for section in menu["sections"]]
        super().__init__(**menu)
