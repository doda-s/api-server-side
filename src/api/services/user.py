from fastapi import Depends, status
from fastapi.exceptions import HTTPException

from pymongo.errors import DuplicateKeyError

from fastapi.exceptions import HTTPException

from api.services.titles import validate_title, get_user_titles_name_description

from api.models.title import Title
from api.dto.user_dto import UserDto
from api.dto.character_dto import CharacterDto
from api.dto.character_dto import CharacterDto
from api.models.user import User
from api.models.character import Character
from api.models.progress import Progress
from api.models.achievement import Achievement
from api.dto.progress_dto import ProgressDto
from api.types.role_names import RoleNames

from typing_extensions import Annotated

async def create_user(username: str, password: str):
    user = User(
        username=username,
        password=password,
        roles=[RoleNames.DEFAULT],
        progress=Progress()
    )
    
    try:
        await user.insert()
    except DuplicateKeyError as dke:
        return {
        "message": "Nome de usuário já está em uso.",
    }
    
    return {
        "message": "Usuário criado com sucesso!",
    }

async def get_user(username: str):
    user = await User.find_one(User.username == username)
    if not user:
        return None
    return user

async def update_user_character(user_dto: UserDto, new_character: CharacterDto):
    character = Character(
        name=new_character.name,
        age=new_character.age,
        gender=new_character.gender,
        profession=new_character.profession,
        role=new_character.role
    )
    user = await User.find_one(User.username==user_dto.username)
    if not user:
        return
    user.character = character
    await user.replace()
    return CharacterDto(**user.character.model_dump())

async def get_user_character(user_dto: UserDto):
    user = await User.find_one(User.username==user_dto.username)
    if not user:
        return None
    return CharacterDto(**user.character.model_dump())

async def update_user_progress(username: str, progress_dto: ProgressDto):
    user = await User.find_one(User.username == username)
    if not user:
        return {"message": "Usuário não encontrado."}
    user.progress = Progress(
        trust= progress_dto.trust,
        number_of_cases_won= progress_dto.number_of_cases_won,
        number_of_lost_cases= progress_dto.number_of_lost_cases,
    )
    await user.replace()
    return UserDto(**user.model_dump())

async def delete_user(current_user: UserDto):
    user = await User.find_one(User.username == current_user.username)
    if not user:
        return
    await user.delete()
    return {"message": "Usuário deletado com sucesso!"}


async def get_user_titles(current_user: UserDto):
    user = await User.find_one(User.username == current_user.username)
    if not user or not user.titles:
        return {"message": "Nenhum título encontrado!"}
    return await get_user_titles_name_description(current_user, user.titles)

async def add_user_titles(current_user: UserDto, title_id: str):
    if not await check_if_has_role(current_user, RoleNames.ADMIN):
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Sem permissão!"
            )
    user = await User.find_one(User.username == current_user.username)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if await validate_title(id): return {"message": "Título não encontrado"}
    if title_id in user.titles:
        return {"message": "O usuário já possui este título!"}
    user.titles.append(title_id)
    try:
        await user.save()
    except Exception as e:
        return {"message": "Erro ao salvar usuário", "error": str(e)}
    return {"message": "Título adicionado com sucesso"}

async def add_achievement_to_user(
    username: str,
    achievement_id: str
):  
    user = await User.find_one(User.username == username)
    achievement = await Achievement.get(achievement_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado!"
        )
    if not achievement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conquista inválida!"
        )
    
    user.achievements.append(str(achievement_id))
    await user.save()
    
    return {"message": "Achievement adicionado com sucesso!"}