from db.connect import client
from bson import ObjectId
from models.menus import Menu, MenuDB
from modules.common import messages
from modules.common.logger import logger


db = client.local.menus


def get(menu_id = None):
    if menu_id:
        if not ObjectId.is_valid(menu_id):
            return False, messages.ERR_SCHEMA.format(err_args="menu_id")
    result = list(db.find({"_id":ObjectId(menu_id)} if menu_id else None))
    if not result:
        return False, messages.ERR_MENU_NOT_FOUND
    data = list(MenuDB(**item).model_dump() for item in result)
    return True, data if len(data) > 1 else data[0]


# TODO: Validar el input antes de guardar en la db para que no se rompa todo.
def update(menu_id: str, data: dict):
    success, result = get(menu_id)
    if not success:
        return False, result
    result.update(data)
    Menu.model_validate(Menu(**result))
    result = db.update_one({"_id": ObjectId(menu_id)}, {"$set": data})
    return True, dict(modified_count=str(result.modified_count))


def new(data: Menu):
    result = db.insert_one(data.model_dump())
    return True, dict(inserted_id=str(result.inserted_id))
