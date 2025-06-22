from pymongo.errors import DuplicateKeyError

from api.dto.achievements_dto import AchievementsDto
from api.models.achievements import Achievements

# Todo: add role verify
async def create_achievements(achievementsDto: AchievementsDto):
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

async def get_all_achievements():
    return await Achievements.find_all().to_list()

async def get_achievements(uuid: str):
    achievements = await Achievements.get(uuid)
    if not achievements:
        return None
    return achievements

# Todo: add role verify
async def update_achievents(uuid: str, achievements_new: AchievementsDto):
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

# Todo: add role verify
async def delete_achievements(uuid: str):
    achievements = await Achievements.get(uuid)
    if not achievements:
        return None
    await achievements.delete()
    return {"message": "achievement deletada com sucesso!"}