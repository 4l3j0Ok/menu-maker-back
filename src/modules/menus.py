from pydantic import ValidationError
from db.connect import client
from bson import ObjectId
from models.menus import Menu, MenuDB
from modules.common import messages
from modules.common.logger import logger

db = client.local.menus


def get(menu_id):
    result = db.find({"_id":ObjectId(menu_id)})
    if not result:
        return False, messages.MENU_NOT_FOUND
    return True, Menu(**result[0])


def update(menu_id: str, data: dict):
    success, menu = get(menu_id)
    if not success:
        return False, result
    menu = menu.model_dump()
    logger.error(menu)
    menu.update(data)
    logger.warning(menu)
    result = db.update_one({"_id": menu_id}, {"$set": data})
    return True, dict(modified_count=str(result.modified_count))


def new(data: Menu):
    result = db.insert_one(data.model_dump())
    return True, dict(inserted_id=str(result.inserted_id))