from fastapi import APIRouter, HTTPException
from models.result import Result
from models.sections import Section
from modules import sections
from modules.common import messages
from typing import Union


router = APIRouter()


@router.get("/")
def get_sections(menu_id: str = None) -> Result:
    """Obtiene la lista de secciones en base al id del menú."""
    success, result = sections.get(menu_id=menu_id, as_dict=True)
    if not success:
        raise HTTPException(status_code=400, detail=result)
    return Result(payload=result, message=messages.MSG_SUCCESS_GENERIC)


@router.post("/new")
def new_section(menu_id: str, section: Union[Section, dict]) -> Result:
    "Agregar una sección a un menú."
    success, result = sections.new(menu_id, section)
    if not success:
        raise HTTPException(status_code=400, detail=result)
    return Result(payload=result, message=messages.MSG_SUCCESS_GENERIC)


@router.put("/update")
async def update_menu(menu_id: str, data: Union[Section, dict]) -> Result:
    "Actualiza la seccion indicada en base al id y los datos nuevos."
    success, result = sections.update(menu_id, data)
    if not success:
        raise HTTPException(status_code=400, detail=result)
    return Result(payload=result, message=messages.MSG_SUCCESS_GENERIC)


@router.delete("/remove")
def remove_section(section_id: str) -> Result:
    "Remueve la sección indicada en base al id del menú y de la sección."
    success, result = sections.remove(section_id)
    if not success:
        raise HTTPException(status_code=400, detail=result)
    return Result(payload=result, message=messages.MSG_SUCCESS_GENERIC)
