from bson import ObjectId
from pydantic import ValidationError
from typing import Union, Tuple
from db.connect import client
from models.menus import Menu, MenuDB
from modules.common import messages
from modules.common.logger import logger
from modules import sections


db = client.local.menus


def get(menu_id = None) -> Tuple[bool, Union[MenuDB, list[MenuDB]]]:
    if menu_id:
        if not ObjectId.is_valid(menu_id):
            return False, messages.ERR_SCHEMA.format(err_args="menu_id")
    result = list(db.find({"_id":ObjectId(menu_id)} if menu_id else None))
    if not result:
        return False, messages.ERR_MENU_NOT_FOUND.format(id=menu_id)
    data = list(MenuDB(**item).model_dump() for item in result)
    return True, data if len(data) > 1 else data[0]


# TODO: Validar el input antes de guardar en la db para que no se rompa todo.
def update(menu_id: str, data: dict) -> Tuple[bool, Union[dict, str]]:
    success, result = get(menu_id)
    if not success:
        return False, result
    result.update(data)
    success, reason = validate(result)
    if not success:
        return False, reason
    result = db.update_one({"_id": ObjectId(menu_id)}, {"$set": data})
    return True, dict(
        modified_count = str(result.modified_count)
    )


def new(data: Menu) -> Tuple[bool, Union[dict, str]]:
    success, reason = validate(data)
    if not success:
        return False, reason
    result = db.insert_one(data.model_dump())
    return True, dict(
        inserted_id = str(result.inserted_id)
    )


def remove(menu_id) -> Tuple[bool, Union[dict, str]]:
    success, result = get(menu_id)
    if not success:
        return False, result
    removed_menus = db.delete_one({"_id": result._id}).deleted_count
    success, result = sections.remove(result.sections)
    if not success:
        logger.error(f"Error al remover las secciones: {result}")
    return True, dict(
        removed_menus = removed_menus,
        removed_sections = result.get("removed_sections", 0),
        removed_products = result.get("removed_products", 0)
    )




def validate(menu, keys=[]):
    try:
        Menu.model_validate(menu)
        if menu.sections:
            for i, section_id in enumerate(menu.sections):
                success, result = sections.get(section_id, index=i)
                if not success:
                    return False, result
        return True, None
    except ValidationError as vex:
        fault_keys = [error["loc"][0] for error in vex.errors() if str(error["loc"][0]) in keys] if keys \
            else [error["loc"][0] for error in vex.errors()]
        if fault_keys:
            return False, messages.ERR_SCHEMA.format(err_args=", ".join(fault_keys))
        return True, None