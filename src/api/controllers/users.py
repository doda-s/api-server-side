# Modelo de controller de usuários

from beanie.exceptions import DocumentNotFound

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from typing_extensions import Annotated

from api.dto.user_dto import UserDto
from api.dto.character_dto import CharacterDto
from api.dto.progress_dto import ProgressDto
from api.middleware.authentication import token_required

from api.services import user as user_service

router = APIRouter()

@router.get("/users/me", response_model=UserDto)
async def read_current_user(
    current_user: Annotated[UserDto, Depends(token_required)]
):
    return current_user

@router.post("/users/me/character/update")
async def update_user_character(
    new_character: CharacterDto,
    current_user: Annotated[UserDto, Depends(token_required)]
):
    try:
        return await user_service.update_user_character(current_user, new_character)
    except DocumentNotFound:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Não foi possível criar o personagem.",
        )

@router.get("/users/me/character", response_model=CharacterDto)
async def user_character(
    current_user: Annotated[UserDto, Depends(token_required)]    
):
    return await user_service.get_user_character(current_user)

@router.post("/users/me/progress/update")
async def update_current_user_progress(
    progress_dto: ProgressDto,
    current_user: Annotated[UserDto, Depends(token_required)]
):
    try:
        return await user_service.update_user_progress(
            current_user.username,
            progress_dto
        )
    except DocumentNotFound:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Não foi possível atualizar o progresso do usuário.",
        )