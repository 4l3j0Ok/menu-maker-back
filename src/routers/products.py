from fastapi import APIRouter
from models.result import Result
from models.products import Product
from modules import products
from modules.common import messages


router = APIRouter()


@router.get("/")
def get_products(section_id: str) -> Result:
    products.get(section_id)


@router.post("/add")
def add_product(section_id: str, product: Product) -> Result:
    products.add(section_id, product)


@router.delete("/remove")
def remove_product(section_id: str, product_id: str) -> Result:
    products.remove(section_id, product_id)
