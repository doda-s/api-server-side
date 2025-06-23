from pymongo.errors import DuplicateKeyError
from fastapi import status
from fastapi.exceptions import HTTPException

from api.dto.achievement_dto import AchievementDto
from api.dto.user_dto import UserDto
from api.models.achievement import Achievement
from api.types.role_names import RoleNames
from api.services.roles import check_if_has_role

# Todo: add role verify
async def create_achievements(
    achievementDto: AchievementDto,
    current_user: UserDto
):
    if await check_if_has_role(current_user=current_user, role=RoleNames.ADMIN):
        achievement = Achievement(
            name=achievementDto.name,
            description=achievementDto.description
        )

        try:
            await achievement.insert()
        except DuplicateKeyError as dke:
            return {
                "message": f"O nome {achievementDto.name} já está em uso.",
            }
        
        return {
            "Achievement criado com sucesso!"
        }
        
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Usuário não autorizado!"
    )

async def get_all_achievements():
    return await Achievement.find_all().to_list()

async def get_achievements(uuid: str):
    achievement = await Achievement.get(uuid)
    if not achievement:
        return None
    return achievement

# Todo: add role verify
async def update_achievents(
    uuid: str,
    achievements_new: AchievementDto,
    current_user: UserDto
):
    if await check_if_has_role(current_user=current_user, role=RoleNames.ADMIN):
        achievement = Achievement(
            name=achievements_new.name,
            description=achievements_new.description
        )
        achievement = await Achievement.get(uuid)
        if not achievement:
            return None
        achievement.name = achievements_new.name
        achievement.description = achievements_new.description
        await achievement.replace()
        return AchievementsDto(**achievement.model_dump())
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Usuário não autorizado!"
    )

# Todo: add role verify
async def delete_achievements(uuid: str, current_user: UserDto):
    if await check_if_has_role(current_user=current_user, role=RoleNames.ADMIN):
        achievement = await Achievement.get(uuid)
        if not achievement:
            return None
        await achievement.delete()
        return {"message": "Achievement deletado com sucesso!"}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Usuário não autorizado!"
    )