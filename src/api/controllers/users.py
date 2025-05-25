# Modelo de controller de usuários

from fastapi import APIRouter, Depends

from typing_extensions import Annotated

from api.dto.user_dto import UserDto
from api.middleware.authentication import get_current_user



router = APIRouter()

@router.get("/users/me", response_model=UserDto)
async def read_current_user(
    current_user: Annotated[UserDto, Depends(get_current_user)]
):
    return current_user