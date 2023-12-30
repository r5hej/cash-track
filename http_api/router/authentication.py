from fastapi import APIRouter
from pydantic import BaseModel

import authentication.auth_controller as auth_controller

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

class LoginDTO(BaseModel):
    username: str
    password: str


class LoginResponseDTO(BaseModel):
    token: str
    expiry_time: str


@router.post("")
def authenticate(payload: LoginDTO) -> LoginResponseDTO:
    session = auth_controller.authenticate(username=payload.username, password=payload.password)
    if session is None:
        raise Exception("login failed?")
    token, expiry_time = session
    return LoginResponseDTO(token=token, expiry_time=expiry_time.strftime("%d/%m/%Y"))
