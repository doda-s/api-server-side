from api.middleware.authentication import token_required
from api.dto.achievements_dto import AchievementsDto
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
@router.get("/achievements/select/{uuid}", response_model=AchievementsDto)
async def get_achievements(uuid: str):
    return await achievements_services.get_achievements(uuid)

# Create achievements
@router.post("/achievements/create")
async def create_achievements(achievements_dto: AchievementsDto):
    return await achievements_services.create_achievements(achievements_dto)

# Update achievements
@router.post("/achievements/update/{uuid}")
async def update_achievements(achievements_dto: AchievementsDto, uuid):
    try:
        return await achievements_services.update_achievents(uuid, achievements_dto)
    except DocumentNotFound:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Não foi possível atualizar o Achievement.",
        )

# Delete achievements
@router.delete("/achievements/delete/{uuid}")
async def delete_achievements(uuid: str):
    return await achievements_services.delete_achievements(uuid)