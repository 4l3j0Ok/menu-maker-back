from fastapi import APIRouter, HTTPException
import modules.users as functions
from models.users import User, Success, Detail
from modules import messages


router = APIRouter()


@router.get("/")
async def get_users(id: str = None) -> Success:
    "Retorna la lista de usuarios o un usuario concreto en base al id."
    success, result = functions.get_users(id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail=Detail(
                payload=None,
                message=result
            )
        )
    return Success(
        input=id if id else None,
        detail=Detail(
            payload=result,
            message=messages.MSG_SUCCESS_GENERIC
        )
    )


@router.post("/save")
async def save_user(user: User) -> Success:
    "Guarda el usuario que sea indicado."
    success, result = functions.save_user(user)
    if not success:
        raise HTTPException(
            status_code=400,
            detail=Detail(
                payload=None,
                message=result
            )
        )
    return Success(
        input=user,
        detail=Detail(
            payload={"id": str(result.inserted_id)},
            message=messages.MSG_SUCCESS_SAVE
        )
    )


@router.put("/update")
async def update_user(user: dict) -> Success:
    "Actualiza el usuario que sea indicado."
    success, result = functions.update_user(user)
    if not success:
        raise HTTPException(
            status_code=400,
            detail=Detail(
                payload=None,
                message=result
            )
        )
    return Success(
        input=user,
        detail=Detail(
            payload=None,
            message=messages.MSG_SUCCESS_SAVE
        )
    )


@router.delete("/remove")
async def remove_user(id: str) -> Success:
    "Remueve el usuario que sea indicado."
    success, result = functions.remove_user(id)
    if not success:
        raise HTTPException(
            status_code=400,
            detail=Detail(
                payload=None,
                message=result
            )
        )
    return Success(
        input=id,
        detail=Detail(
            payload={"deleted_id": id},
            message=messages.MSG_SUCCESS_GENERIC
        ))
