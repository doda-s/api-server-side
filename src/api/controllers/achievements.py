from api.middleware.authentication import token_required
from api.dto.achievement_dto import AchievementDto
from api.dto.user_dto import UserDto
from api.services import achievements as achievements_services

from typing_extensions import Annotated

from beanie.exceptions import DocumentNotFound
from fastapi.exceptions import HTTPException

from fastapi import Depends, status, APIRouter

router = APIRouter()

# Select all achievements
@router.get("/achievements")
async def get_all_achievements():
    return await achievements_services.get_all_achievements()

# Select achievements by uuid
@router.get("/achievements/select/{uuid}", response_model=AchievementDto)
async def get_achievements(uuid: str):
    return await achievements_services.get_achievements(uuid)

# Create achievements
@router.post("/achievements/create")
async def create_achievements(
    achievements_dto: AchievementDto,
    current_user: Annotated[UserDto, Depends(token_required)]
):
    return await achievements_services.create_achievements(
        achievements_dto,
        current_user
    )

# Update achievements
@router.put("/achievements/update/{uuid}")
async def update_achievements(
    achievements_dto: AchievementDto, uuid,
    current_user: Annotated[UserDto, Depends(token_required)]
):
    try:
        return await achievements_services.update_achievents(
            uuid,
            achievements_dto,
            current_user
        )
    except DocumentNotFound:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Não foi possível atualizar o Achievement.",
        )

# Delete achievements
@router.delete("/achievements/delete/{uuid}")
async def delete_achievements(
    uuid: str,
    current_user: Annotated[UserDto, Depends(token_required)]
):
    return await achievements_services.delete_achievements(uuid, current_user)