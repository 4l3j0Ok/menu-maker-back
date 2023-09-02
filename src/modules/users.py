from modules import messages
from models.users import User
from pydantic import ValidationError
from db.client import client
from bson import ObjectId


db = client.local.users


def validate_user(user, keys=[]):
    try:
        User.validate(User(**user)) if isinstance(user, dict) else User.validate(user)
        return True, None
    except ValidationError as vex:
        fault_keys = [error["loc"][0] for error in vex.errors() if str(error["loc"][0]) in keys] if keys \
            else [error["loc"][0] for error in vex.errors()]
        if fault_keys:
            return False, messages.ERR_SCHEMA.format(err_args=", ".join(fault_keys))
        return True, None


def get_users(id: str = None):
    if id:
        if not ObjectId.is_valid(id):
            return False, messages.ERR_SCHEMA.format(err_args="id")
    result = list(db.find({"_id":ObjectId(id)} if id else None))
    if not result:
        return False, messages.ERR_USER_NOT_FOUND
    user_list = [User(**user) for user in result]
    return True, user_list if len(user_list) != 1 else user_list[0]


def save_user(user):
    success, result = validate_user(user)
    if not success:
        return False, result
    if user.id:
        if get_users(user.id)[0]:
            return False, messages.ERR_USER_ALREADY_EXISTS.format(id=user.id)
    del user.id
    result = db.insert_one(user.dict())
    return True, result


def update_user(user):
    success, result = validate_user(user, keys=["id"])
    if not success:
        return False, str(result)
    success, current_user = get_users(id=user["id"])
    if not success:
        return False, current_user
    del user["id"]
    result = db.update_one({"_id": ObjectId(current_user.id)}, {"$set": user})
    return True, result


def remove_user(id):
    success, current_user = get_users(id)
    if not success:
        return False, current_user
    result = db.delete_many({"_id": ObjectId(current_user.id)})
    return True, result
