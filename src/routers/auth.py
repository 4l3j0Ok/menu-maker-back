from fastapi import APIRouter, HTTPException, Depends
import modules.auth as auth
from models.user import Success, Detail
from modules import messages
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer


router = APIRouter()
oauth_scheme = OAuth2PasswordBearer(tokenUrl="/token")


@router.post("/get_token")
async def get_token(form: OAuth2PasswordRequestForm = Depends()) -> Success:
    "Login."
    success, result = auth.get_token(form)
    if not success:
        raise HTTPException(
            status_code=403,
            payload=Detail(
                payload=None,
                message=result
            )
        )
    return Success(
        payload=Detail(
            payload={"id": str(result.inserted_id)},
            message=messages.MSG_SUCCESS_SAVE
        )
    )


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()) -> Success:
    "Login."
    success, result = auth.login(form)
    if not success:
        raise HTTPException(
            status_code=403,
            payload=Detail(
                payload=None,
                message=result
            )
        )
    return Success(
        payload=Detail(
            payload={"id": str(result.inserted_id)},
            message=messages.MSG_SUCCESS_SAVE
        )
    )

@router.post("/register")
def register(user: User) -> Success:
    "Guarda el usuario que sea indicado."
    success, result = auth.save_user(user)
    if not success:
        raise HTTPException(
            status_code=400,
            payload=Detail(
                payload=None,
                message=result
            )
        )
    return Success(
        input=user,
        payload=Detail(
            payload={"id": str(result.inserted_id)},
            message=messages.MSG_SUCCESS_SAVE
        )
    )