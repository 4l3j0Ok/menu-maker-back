from bson import ObjectId
from typing import Union, Tuple
from pydantic import ValidationError
from db.connect import client
from models.products import Product, ProductDB
from modules.common import messages
from modules.common.logger import logger
from modules import sections


db = client.local.products


def get(
        section_id: Union[str, ObjectId] = None,
        product_ids: Union[str, list[str], ObjectId, list[ObjectId]] = None,
        as_dict: bool = False
    ) -> Tuple[bool, Union[ProductDB, list[ProductDB]]]:
    query = {}
    if section_id:
        success, section = sections.get(section_ids=section_id)
        if not success:
            return False, section
        query = {"_id": {"$in": [ObjectId(product) for product in section.products]}}
    elif product_ids:
        product_ids = product_ids if isinstance(product_ids, list) else [product_ids]
        product_ids = product_ids if isinstance(product_ids[0], ObjectId) \
            else [ObjectId(product_id) for product_id in product_ids]
        query = {"_id": {"$in": product_ids}}
    logger.info(f"Ejecutando find: {query}")
    products = list(db.find(query))
    if not products:
        return True, []
    data = list(ProductDB(**item) for item in products) if not as_dict \
        else list(ProductDB(**item).model_dump() for item in products)
    return True, data if len(data) > 1 else data[0]


def new(section_id: str, product: Union[dict, Product]) -> Tuple[bool, Union[dict, str]]:
    product = product if isinstance(product, dict) else product.model_dump()
    success, reason = validate(product)
    if not success:
        return False, reason
    logger.info(f"Ejecutando insert_one: {product}")
    db_result = db.insert_one(product)
    success, result = sections.append_product(section_id, db_result.inserted_id)
    if not success:
        logger.error(result)
        return False, result
    return True, db_result


def update(product_id: str, data: dict) -> Tuple[bool, Union[dict, str]]:
    success, product = get(product_id, as_dict=True)
    if not success:
        return False, product
    product.update(data)
    success, reason = validate(product)
    if not success:
        return False, reason
    query = ({"_id": ObjectId(product_id)}, {"$set": data})
    logger.info(f"Ejecutando update_one: {query}")
    db_result = db.update_one(*query)
    return True, dict(
        modified_count = str(db_result.modified_count)
    )


def remove(product_ids) -> Tuple[bool, Union[dict, str]]:
    success, product = get(product_ids=product_ids)
    if not success:
        logger.error(f"Error al remover : {product}")
        return False, product
    query = {"_id": ObjectId(product.id)}
    logger.info(f"Ejecutando delete_one: {query}")
    removed_products = db.delete_one(query).deleted_count
    data = dict(
        removed_products = removed_products
    )
    return True, data


def validate(product, ignored_keys=[]):
    try:
        Product.model_validate(product)
        return True, None
    except ValidationError as vex:
        fault_keys = [error["loc"][0] for error in vex.errors() if str(error["loc"][0]) not in ignored_keys]
        if fault_keys:
            return False, messages.ERR_SCHEMA.format(err_args=", ".join(fault_keys))
        return True, None

