from fastapi import APIRouter, HTTPException, Depends
import modules.user as functions
from models.user import Success, Detail
from modules import messages
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()) -> Success:
    "Login."
    success, result = functions.login(form)
    if not success:
        raise HTTPException(
            status_code=403,
            detail=Detail(
                payload=None,
                message=result
            )
        )
    return Success(
        detail=Detail(
            payload={"id": str(result.inserted_id)},
            message=messages.MSG_SUCCESS_SAVE
        )
    )