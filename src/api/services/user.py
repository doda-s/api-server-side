from fastapi import Depends

from pymongo.errors import DuplicateKeyError

from api.dto.user_dto import UserDto
from api.dto.character_dto import CharacterDto
from api.dto.character_dto import CharacterDto
from api.models.user import User
from api.models.character import Character
from api.models.progress import Progress
from api.dto.progress_dto import ProgressDto

from typing_extensions import Annotated

async def create_user(username: str, password: str):
    user = User(
        username=username,
        password=password,
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