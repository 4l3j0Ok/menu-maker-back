from fastapi import APIRouter
from models.menus import Menu
from modules import menus
from modules.common import messages


router = APIRouter()

@router.get("/")
def get_sections(menu_id):
    return 