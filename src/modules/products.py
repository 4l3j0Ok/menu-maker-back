from models.products import Product, ProductDB
from modules.common import messages
from modules.common.logger import logger
from db.connect import client
from bson import ObjectId


db = client.local.products


def get(section_id):
    if not ObjectId.is_valid(section_id):
        return False, messages.ERR_SCHEMA.format(err_args="section_id")
    result = list(db.find({"section_id": section_id}))
    if not result:
        return False, messages.ERR_PRODUCT_NOT_FOUND
    data = list(ProductDB(**item).model_dump() for item in result)
    return True, data if len(data) > 1 else data[0]


def add(section_id, data: Product):
    if not ObjectId.is_valid(section_id):
        return False, messages.ERR_SCHEMA.format(err_args="section_id")
    data.section_id = section_id
    Product.model_validate(data)
    result = db.insert_one(data.model_dump())
    return True, dict(inserted_id=str(result.inserted_id))