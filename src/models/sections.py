from pydantic import BaseModel, Field
from typing import Union, Optional
from bson import ObjectId
from models.products import Product


class Section(BaseModel):
    name: str
    description: str
    products: Union[list[str], None] = Field(example=["507f1f77bcf86cd799439011", "00000020f51bb4362eee2a4d"])
    img: Union[str, None] = Field(example="https://example.com/")


class SectionDB(Section):
    id: str
    menu_id: str

    def __init__(self, **section):
        if "_id" in section and isinstance(section["_id"], ObjectId):
            section["id"] = str(section["_id"])
        if "products" in section:
            section["products"] = [str(product) for product in section["products"]]
        if "menu_id" in section and isinstance(section["menu_id"], ObjectId):
            section["menu_id"] = str(section["menu_id"])
        super().__init__(**section)