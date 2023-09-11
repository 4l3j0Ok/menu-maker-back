from modules.common import messages
from models.user import User, UserDB
from pydantic import ValidationError
from db.connect import client
from bson import ObjectId


db = client.local.users


def validate(user, keys=[]):
    try:
        User.model_validate(User(**user)) if isinstance(user, dict) else User.model_validate(user)
        return True, None
    except ValidationError as vex:
        fault_keys = [error["loc"][0] for error in vex.errors() if str(error["loc"][0]) in keys] if keys \
            else [error["loc"][0] for error in vex.errors()]
        if fault_keys:
            return False, messages.ERR_SCHEMA.format(err_args=", ".join(fault_keys))
        return True, None


def get(**params):
    result = list(db.find({params}))
    if not result:
        return False, messages.ERR_USER_NOT_FOUND
    user_list = [User(**user) for user in result]
    return True, user_list if len(user_list) != 1 else user_list[0]


def save(user: UserDB):
    success, result = validate(user)
    if not success:
        return False, result
    if user.id:
        if get(user.id)[0]:
            return False, messages.ERR_USER_ALREADY_EXISTS.format(id=user.id)
    del user.id
    result = db.insert_one(user.model_dump())
    return True, result


def update(user):
    success, result = validate(user, keys=["id"])
    if not success:
        return False, str(result)
    success, current_user = get(id=user["id"])
    if not success:
        return False, current_user
    del user["id"]
    result = db.update_one({"_id": ObjectId(current_user.id)}, {"$set": user})
    return True, result


def remove(id):
    success, current_user = get(id)
    if not success:
        return False, current_user
    result = db.delete_many({"_id": ObjectId(current_user.id)})
    return True, result
