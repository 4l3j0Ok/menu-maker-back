from modules.common import messages
from models.user import User, UserDB
from pydantic import Union, Tuple
from db.connect import client
from bson import ObjectId
from modules.common.logger import logger


db = client.menu_maker.users


def get(
        user_ids: Union[str, list[str]],
        query: Union[dict, None] = {},
        as_dict: bool = False
    ) -> Tuple[bool, Union[dict, list[dict]]]:
    if user_ids:
        user_ids = user_ids if isinstance(user_ids, list) else [user_ids]
        for user_id in user_ids:
            if not ObjectId.is_valid(user_id):
                return False, messages.ERR_SCHEMA.format(err_args="user_id")
        parsed_ids = [ObjectId(user_id) for user_id in user_ids]
        query = {"_id": {"$in": parsed_ids}}
    logger.info(f"Ejecutando find: {query}")
    users = list(db.find(query))
    if not users:
        if not user_ids:
            return False, messages.ERR_EMPTY_COLLECTION
        return False, messages.ERR_USER_NOT_FOUND.format(id=user_ids[0])
    data = list(UserDB(**item) for item in users) if not as_dict \
        else list(UserDB(**item).model_dump() for item in users)
    return True, data if len(data) > 1 else data[0]

