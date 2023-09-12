from fastapi import APIRouter
from models.result import Result
from modules import products
from modules.common import messages


router = APIRouter()


@router.get("/")
def get_products(section_id) -> Result:
    return 