from fastapi import APIRouter
from models.menus import Menu
from models.response import Response
from modules import menus
from modules.common import messages


router = APIRouter()


@router.get("/")
async def get_menu(menu_id: str) -> Response:
    success, result = menus.get(menu_id)
    if not success:
        return Response(success=success, message=result)
    return Response(success=success, payload=result, message=messages.MSG_SUCCESS_GENERIC)


@router.put("/update")
async def update_menu(menu_id: str, data: dict) -> Response:
    success, result = menus.update(menu_id, data)
    if not success:
        return Response(success=success, message=result)
    return Response(success=success, payload=result, message=messages.MSG_SUCCESS_GENERIC)


@router.post("/new")
async def new_menu(data: Menu) -> Response:
    success, result = menus.new(data)
    if not success:
        return Response(success=success, message=result)
    return Response(success=success, payload=result, message=messages.MSG_SUCCESS_GENERIC)
