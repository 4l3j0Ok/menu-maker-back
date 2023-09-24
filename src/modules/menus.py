from bson import ObjectId
from pydantic import ValidationError
from typing import Union, Tuple
from db.connect import client
from models.menus import Menu, MenuDB
from modules.common import messages
from modules.common.logger import logger
from modules import sections


db = client.local.menus


def get(menu_ids: Union[str, list[str]], as_dict: bool = False) -> Tuple[bool, Union[dict, list[dict]]]:
    query = {}
    if menu_ids:
        menu_ids = menu_ids if isinstance(menu_ids, list) else [menu_ids]
        for menu_id in menu_ids:
            if not ObjectId.is_valid(menu_id):
                return False, messages.ERR_SCHEMA.format(err_args="menu_id")
        parsed_ids = [ObjectId(menu_id) for menu_id in menu_ids]
        query = {"_id": {"$in": parsed_ids}}
    result = list(db.find(query))
    if not result:
        if not menu_ids:
            return False, messages.ERR_EMPTY_COLLECTION
        return False, messages.ERR_MENU_NOT_FOUND.format(id=menu_ids[0])
    data = list(MenuDB(**item) for item in result) if not as_dict \
        else list(MenuDB(**item).model_dump() for item in result)
    return True, data if len(data) > 1 else data[0]


def update(menu_id: str, data: dict) -> Tuple[bool, Union[dict, str]]:
    success, menu = get(menu_id, as_dict=True)
    if not success:
        return False, menu
    menu.update(data)
    success, reason = validate(menu)
    if not success:
        return False, reason
    db_result = db.update_one({"_id": ObjectId(menu_id)}, {"$set": data})
    return True, dict(
        modified_count = str(db_result.modified_count)
    )


def new(menu: Union[dict, Menu]) -> Tuple[bool, Union[dict, str]]:
    menu = menu if isinstance(menu, dict) else menu.model_dump()
    success, reason = validate(menu, ignored_keys=["sections"] if not menu.get("sections") else [])
    if not success:
        return False, reason
    menu["sections"] = menu.get("sections", [])
    if menu["sections"]:
        success, result = sections.get(section_ids=menu["sections"])
        logger.error(menu["sections"])
        if not success:
            return False, result
    result = db.insert_one(menu)
    return True, dict(
        inserted_id = str(result.inserted_id)
    )


def remove(menu_id) -> Tuple[bool, Union[dict, str]]:
    success, menu = get(menu_id)
    if not success:
        return False, menu
    removed_menus = db.delete_one({"_id": ObjectId(menu.id)}).deleted_count
    data = dict(
        removed_menus = removed_menus,
        removed_sections = 0,
        removed_products = 0
    )
    if menu.sections:
        success, result = sections.remove(menu.sections)
        if not success:
            logger.error(f"Error al remover las secciones: {result}")
            return False, result
        data.update(result)
    return True, data


def validate(menu, ignored_keys=[]):
    try:
        Menu.model_validate(menu)
        menu = Menu(**menu)
        if menu.sections:
            success, result = sections.get(section_ids=menu.sections)
            if not success:
                return False, result
        return True, None
    except ValidationError as vex:
        fault_keys = [error["loc"][0] for error in vex.errors() if str(error["loc"][0]) not in ignored_keys]
        if fault_keys:
            return False, messages.ERR_SCHEMA.format(err_args=", ".join(fault_keys))
        return True, None


def append_section(menu_id: str, section_id: Union[str, ObjectId]):
    section_id = section_id if isinstance(section_id, ObjectId) else ObjectId(section_id)
    success, result = get(menu_id)
    if not success:
        return False, result
    result = db.update_one({"_id": ObjectId(menu_id)}, {"$push": {"sections": section_id}})
    return True, dict(
        modified_count = str(result.modified_count)
    )
