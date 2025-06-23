from pymongo.errors import DuplicateKeyError
from fastapi import status
from fastapi.exceptions import HTTPException

from api.dto.achievements_dto import AchievementsDto
from api.dto.user_dto import UserDto
from api.models.achievements import Achievements
from api.types.role_names import RoleNames
from api.services.roles import check_if_has_role

# Todo: add role verify
async def create_achievements(
    achievementsDto: AchievementsDto,
    current_user: UserDto
):
    if await check_if_has_role(current_user=current_user, role=RoleNames.ADMIN):
        achievements = Achievements(
            name=achievementsDto.name,
            description=achievementsDto.description
        )

        try:
            await achievements.insert()
        except DuplicateKeyError as dke:
            return {
                "message": "Nome de usuário já está em uso.",
            }
        
        return {
            "Achievements criado com sucesso"
        }
        
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Usuário não autorizado!"
    )

async def get_all_achievements():
    return await Achievements.find_all().to_list()

async def get_achievements(uuid: str):
    achievements = await Achievements.get(uuid)
    if not achievements:
        return None
    return achievements

# Todo: add role verify
async def update_achievents(
    uuid: str,
    achievements_new: AchievementsDto,
    current_user: UserDto
):
    if await check_if_has_role(current_user=current_user, role=RoleNames.ADMIN):
        achievements = Achievements(
            name=achievements_new.name,
            description=achievements_new.description
        )
        achievements = await Achievements.get(uuid)
        if not achievements:
            return None
        achievements.name = achievements_new.name
        achievements.description = achievements_new.description
        await achievements.replace()
        return AchievementsDto(**achievements.model_dump())
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Usuário não autorizado!"
    )

# Todo: add role verify
async def delete_achievements(uuid: str, current_user: UserDto):
    if await check_if_has_role(current_user=current_user, role=RoleNames.ADMIN):
        achievements = await Achievements.get(uuid)
        if not achievements:
            return None
        await achievements.delete()
        return {"message": "achievement deletada com sucesso!"}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Usuário não autorizado!"
    )