from pydantic import BaseModel
from typing import Union, Optional
from bson import ObjectId
from models.products import Product


class Section(BaseModel):
    name: str


class SectionDB(Section):
    id: str
    products: list[str]

    def __init__(self, **section):
        if "_id" in section and isinstance(section["_id"], ObjectId):
            section["id"] = str(section["_id"])
        super().__init__(**section)