from bson import ObjectId
from typing import Union, Tuple
from models.products import Product, ProductDB
from modules.common import messages
from modules.common.logger import logger
from modules import sections
from db.connect import client


db = client.local.products


def get(
        section_id: Union[str, ObjectId] = None,
        product_ids: Union[str, list[str], ObjectId, list[ObjectId]] = None,
        as_dict: bool = False
    ) -> Tuple[bool, Union[ProductDB, list[ProductDB]]]:
    query = {}
    if section_id:
        success, result = sections.get(section_id)
        if not success:
            return result
        query = {"_id": {"$in": result.products}}
    elif product_ids:
        product_ids = product_ids if isinstance(product_ids, list) else [product_ids]
        product_ids = product_ids if isinstance(product_ids[0], ObjectId) \
            else [ObjectId(product_id) for product_id in product_ids]
        query = {"_id": {"$in": product_ids}}
    sections = list(db.find(query))
    if not sections:
        return False, messages.ERR_SECTIONS_NOT_FOUND
    data = list(ProductDB(**item) for item in result) if not as_dict \
        else list(ProductDB(**item).model_dump() for item in result)
    return True, data if len(data) > 1 else data[0]


def add(section_id, data: Product):
    if not ObjectId.is_valid(section_id):
        return False, messages.ERR_SCHEMA.format(err_args="section_id")
    data.section_id = section_id
    Product.model_validate(data)
    result = db.insert_one(data.model_dump())
    return True, dict(inserted_id=str(result.inserted_id))


def remove(product_ids) -> Tuple[bool, Union[dict, str]]:
    success, result = get(product_ids=product_ids)
    if not success:
        logger.error(f"Error al remover los productos: {result}")
        return False, result
    removed_products = db.delete_one({"_id": result._id}).deleted_count
    data = dict(removed_products = removed_products)
    return True, data
