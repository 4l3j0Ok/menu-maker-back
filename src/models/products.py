from pydantic import BaseModel
from pydantic import HttpUrl
from bson import ObjectId


class Product(BaseModel):
    name: str
    description: str
    price: int
    img: HttpUrl


class ProductDB(Product):
    id: str

    def __init__(self, **product):
        if "_id" in product and isinstance(product["_id"], ObjectId):
            product["id"] = str(product["_id"])
        super().__init__(**product)