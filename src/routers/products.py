from fastapi import APIRouter, HTTPException
from typing import Union
from models.result import Result
from models.products import Product
from modules import products
from modules.common import messages


router = APIRouter()


@router.get("/")
def get_products(section_id: str) -> Result:
    "Obtiene la lista de productos de una sección en base al id."
    success, result = products.get(section_id, as_dict=True)
    if not success:
        raise HTTPException(status_code=400, detail=result)
    return Result(payload=result, message=messages.MSG_SUCCESS_GENERIC)


@router.post("/new")
def new_product(section_id: str, product: Product) -> Result:
    "Agregar un producto a una sección"
    success, result = products.new(section_id, product)
    if not success:
        raise HTTPException(status_code=400, detail=result)
    return Result(payload=result, message=messages.MSG_SUCCESS_GENERIC)


@router.put("/update")
async def update_menu(menu_id: str, data: Union[Product, dict]) -> Result:
    "Actualiza el producto indicado en base al id y los datos nuevos."
    success, result = products.update(menu_id, data)
    if not success:
        raise HTTPException(status_code=400, detail=result)
    return Result(payload=result, message=messages.MSG_SUCCESS_GENERIC)


@router.delete("/remove")
def remove_product(product_id: str) -> Result:
    "Remueve la sección indicada en base al id de la sección y del producto."
    success, result = products.remove(product_id)
    if not success:
        raise HTTPException(status_code=400, detail=result)
    return Result(payload=result, message=messages.MSG_SUCCESS_GENERIC)
