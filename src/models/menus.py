from pydantic import BaseModel
from typing import Union, Optional
from bson import ObjectId


class Product(BaseModel):
    name: str
    description: str
    price: int


class Section(BaseModel):
    name: str
    product: Optional[list[Product]]


class Menu(BaseModel):
    name: str
    description: str
    sections: Optional[list[Section]] = []


class MenuDB(Menu):
    id: Union[str, None]

    def __init__(self, **menu):
        if "_id" in menu and isinstance(menu["_id"], ObjectId):
            menu["id"] = str(menu["_id"])
        super().__init__(**menu)
