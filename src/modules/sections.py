from bson import ObjectId
from pydantic import ValidationError
from db.connect import client
from models.sections import Section, SectionDB
from modules.common import messages
from modules.common.logger import logger


db = client.local.sections


def get(section_id, index = None):
    if not ObjectId.is_valid(section_id):
        return False, messages.ERR_SCHEMA.format(
            err_args="sections{}".format(
                f"[{index}]" if index != None else ""
            )
        )
    result = list(db.find({"_id":ObjectId(section_id)} if section_id else None))
    if not result:
        return False, messages.ERR_SECTION_NOT_FOUND.format(id=section_id)
    data = SectionDB(**result[0]).model_dump()
    return True, data
