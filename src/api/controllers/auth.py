from api.services.user import create_user
from api.dto.user_auth_dto import UserAuthDto
from api.dto.token import Token
from api.middleware.authentication import authenticate_user
from api.middleware.authentication import get_password_hash
from api.middleware.authentication import create_access_token

from config import Config

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from typing_extensions import Annotated


router = APIRouter()

@router.post("/auth/register")
async def register_user(user_auth_dto: UserAuthDto):
    return await create_user(
        user_auth_dto.username,
        get_password_hash(user_auth_dto.password)
    )

@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()])->Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    accses_token = create_access_token(
        data={"sub":user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=accses_token, token_type="bearer")