from pydantic import BaseModel, Field
from typing import Union
from bson import ObjectId


class Product(BaseModel):
    name: str
    description: str
    price: int
    img: Union[str, None] = Field(example="https://example.com/")


class ProductDB(Product):
    id: str

    def __init__(self, **product):
        if "_id" in product and isinstance(product["_id"], ObjectId):
            product["id"] = str(product["_id"])
        super().__init__(**product)