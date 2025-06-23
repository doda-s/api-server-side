from api.middleware.authentication import token_required

from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends, status

from beanie.exceptions import DocumentNotFound

from api.dto.title_dto import TitleDto
from api.dto.user_dto import UserDto

from api.services import titles as title_service

from typing_extensions import Annotated

router = APIRouter()

@router.post("/titles/add")
async def add_title(
    title: TitleDto,
    current_user: Annotated[UserDto, Depends(token_required)]
):
    try:
        return await title_service.add_title(current_user, title)
    except DocumentNotFound:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Não foi possível criar o título.",
        )

@router.get("/titles")
async def get_all_titles(
    current_user: Annotated[UserDto, Depends(token_required)]    
):
    return await title_service.get_all_titles(current_user)

@router.get("/titles/id/{id}")
async def get_title_by_id(
    current_user: Annotated[UserDto, Depends(token_required)],
    id: str
):
    return await title_service.get_title_by_id(current_user,id)