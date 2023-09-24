from bson import ObjectId
from typing import Union, Tuple
from pydantic import ValidationError
from db.connect import client
from models.sections import Section, SectionDB
from modules.common import messages
from modules.common.logger import logger
from modules import products, menus


db = client.menu_maker.sections


def get(
        section_ids: Union[str, list[str], ObjectId, list[ObjectId]] = None,
        menu_id: Union[str, ObjectId] = None,
        as_dict: bool = False
    ) -> Tuple[bool, Union[SectionDB, list[SectionDB]]]:
    query = {}
    if menu_id:
        if not ObjectId.is_valid(menu_id):
            return False, messages.ERR_SCHEMA.format(err_args="menu_id")
        query = {"menu_id": {"$in": [ObjectId(menu_id)]}}
    elif section_ids:
        section_ids = section_ids if isinstance(section_ids, list) else [section_ids]
        section_ids = section_ids if isinstance(section_ids[0], ObjectId) \
            else [ObjectId(section_id) for section_id in section_ids]
        query = {"_id": {"$in": section_ids}}
    logger.info(f"Ejecutando find: {query}")
    sections = list(db.find(query))
    if not sections:
        if not section_ids:
            return False, messages.ERR_EMPTY_COLLECTION
        return False, messages.ERR_SECTIONS_NOT_FOUND
    data = list(SectionDB(**item) for item in sections) if not as_dict \
        else list(SectionDB(**item).model_dump() for item in sections)
    return True, data if len(data) > 1 else data[0]


def new(menu_id: str, section: Union[dict, Section]) -> Tuple[bool, Union[dict, str]]:
    section = section if isinstance(section, dict) else section.model_dump()
    menu_id = menu_id if isinstance(menu_id, ObjectId) else ObjectId(menu_id)
    success, menu = menus.get(menu_id)
    if not success:
        return False, menu
    success, reason = validate(section, ignored_keys=["products"] if not section.get("products") else [])
    if not success:
        return False, reason
    section["products"] = section.get("products", [])
    section["menu_id"] = menu_id
    db_result = db.insert_one(section)
    success, result = menus.append_section(menu_id, db_result.inserted_id)
    if not success:
        logger.error(result)
        return False, result
    return True, dict(
        inserted_id = str(db_result.inserted_id)
    )


def update(section_id: str, data: dict) -> Tuple[bool, Union[dict, str]]:
    success, section = get(section_id, as_dict=True)
    if not success:
        return False, section
    section.update(data)
    success, reason = validate(section)
    if not success:
        return False, reason
    db_result = db.update_one({"_id": ObjectId(section_id)}, {"$set": data})
    return True, dict(
        modified_count = str(db_result.modified_count)
    )


def remove(section_id, from_remove: bool = False) -> Tuple[bool, Union[dict, str]]:
    section_id = section_id if isinstance(section_id, ObjectId) else ObjectId(section_id)
    success, section = get(section_id)
    if not success:
        logger.error(f"Error al remover las secciones: {section}")
        return False, section
    removed_sections = db.delete_one({"_id": section_id}).deleted_count
    data = dict(
        removed_sections = removed_sections,
        removed_products = 0
    )
    if section.products:
        success, result = products.remove(section.products, from_remove=True)
        logger.info(f"Resultado de remover los productos: {result}")
        if success:
            data.update(result)
    if not from_remove:
        success, result = menus.remove_section(section.menu_id, section_id)
        if not success:
            logger.error(result)
    return True, data


def validate(section, ignored_keys=[]):
    try:
        Section.model_validate(section)
        if section.products:
            for i, products_id in enumerate(section.products):
                success, product = products.get(products_id, index=i)
                if not success:
                    return False, product
        return True, None
    except ValidationError as vex:
        fault_keys = [error["loc"][0] for error in vex.errors() if str(error["loc"][0]) not in ignored_keys]
        if fault_keys:
            return False, messages.ERR_SCHEMA.format(err_args=", ".join(fault_keys))
        return True, None



def append_product(section_id: Union[str, ObjectId], product_id: Union[str, ObjectId]):
    section_id = section_id if isinstance(section_id, ObjectId) else ObjectId(section_id)
    product_id = product_id if isinstance(product_id, ObjectId) else ObjectId(product_id)
    success, section = get(section_id)
    if not success:
        return False, section
    db_result = db.update_one({"_id": section_id}, {"$push": {"products": product_id}})
    return True, dict(
        modified_count = str(db_result.modified_count)
    )


def remove_product(section_id: str, product_id: Union[str, ObjectId]):
    product_id = product_id if isinstance(product_id, ObjectId) else ObjectId(product_id)
    result = db.update_one({"_id": ObjectId(section_id)}, {"$pull": {"sections": product_id}})
    return True, dict(
        modified_count = str(result.modified_count)
    )
