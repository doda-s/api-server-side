# Modelo de controller de usuários

from fastapi import APIRouter

from api.dto.user_dto import UserDto

from api.models.user import User

router = APIRouter()

# exemplo de end point com parâmetro
@router.get("/user/{username}")
async def get_user_by_name(username: str):
    return {"message": f"Hello, {username}!"}

# exemplo de endpoint com parâmetro e query
@router.get("/user/{username}/")
def get_username_info(username = "", filter_type: str = "len"):
    if username == "":
        return {"message": "Nenhum nome foi passado como parâmetro."}
    
    if filter_type == "len":
        return {"message": f"Tamano no nome {username}: {len(username)}"}
    
    return {"message": "Nenhum tipo de filtro foi passado na query."}

@router.post('/user/create')
async def create_user(user_dto: UserDto):
    user = User(
        username=user_dto.username,
        password=user_dto.password
    )
    await user.insert()
    
    return {
        "message": "Usuário criado com sucesso!",
    }