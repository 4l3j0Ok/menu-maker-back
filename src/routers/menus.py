from fastapi import APIRouter, HTTPException
from models.menus import Menu
from models.result import Result
from modules import menus
from modules.common import messages
from typing import Union


router = APIRouter()


@router.get("/")
async def get_menus(menu_id: str = None) -> Result:
    "Obtiene la lista de menús o el menú indicado en base al id."
    success, result = menus.get(menu_id, as_dict=True)
    if not success:
        raise HTTPException(status_code=400, detail=result)
    return Result(payload=result, message=messages.MSG_SUCCESS_GENERIC)


@router.post("/new")
async def new_menu(menu: Union[Menu, dict]) -> Result:
    "Añade el menú indicado."
    success, result = menus.new(menu)
    if not success:
        raise HTTPException(status_code=400, detail=result)
    return Result(payload=result, message=messages.MSG_SUCCESS_GENERIC)


@router.put("/update")
async def update_menu(menu_id: str, data: Union[Menu, dict]) -> Result:
    "Actualiza el menú indicado en base al id."
    success, result = menus.update(menu_id, data)
    if not success:
        raise HTTPException(status_code=400, detail=result)
    return Result(payload=result, message=messages.MSG_SUCCESS_GENERIC)


@router.delete("/remove")
def remove_menu(menu_id: str) -> Result:
    "Remueve el menú indicado y sus objetos relacionados en base al id."
    success, result = menus.remove(menu_id)
    if not success:
        raise HTTPException(status_code=400, detail=result)
    return Result(payload=result, message=messages.MSG_SUCCESS_GENERIC)