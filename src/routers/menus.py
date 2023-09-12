from fastapi import APIRouter, HTTPException, Response
from models.menus import Menu
from models.result import Result
from modules import menus
from modules.common import messages
from typing import Union



router = APIRouter()


@router.get("/")
async def get_menus(menu_id: str = None) -> Result:
    success, result = menus.get(menu_id)
    if not success:
        raise HTTPException(status_code=400, detail=result)
    return Result(payload=result, message=messages.MSG_SUCCESS_GENERIC)


@router.put("/update")
async def update_menu(menu_id: str, data: Union[Menu, dict]) -> Result:
    success, result = menus.update(menu_id, data)
    if not success:
        raise HTTPException(status_code=400, detail=result)
    return Result(payload=result, message=messages.MSG_SUCCESS_GENERIC)


@router.post("/new")
async def new_menu(data: Menu) -> Result:
    success, result = menus.new(data)
    if not success:
        return Response(success=success, message=result)
    return Result(payload=result, message=messages.MSG_SUCCESS_GENERIC)
