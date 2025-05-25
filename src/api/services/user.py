from fastapi import Depends

from pymongo.errors import DuplicateKeyError

from api.dto.user_auth_dto import UserAuthDto
from api.models.user import User

from typing_extensions import Annotated

async def create_user(username: str, password: str):
    user = User(
        username=username,
        password=password
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