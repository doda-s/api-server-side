from pymongo.errors import DuplicateKeyError

from api.dto.user_auth_dto import UserAuthDto

from api.models.user import User

async def create_user(user_auth_dto: UserAuthDto):
    user = User(
        username=user_auth_dto.username,
        password=user_auth_dto.password
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