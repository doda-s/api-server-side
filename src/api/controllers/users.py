# Modelo de controller de usuários

from fastapi import APIRouter

router = APIRouter()

# exemplo de end point com parâmetro
@router.get("/user/{username}")
async def get_user_by_name(username: str):
    return {"message": f"Hello, {username}!"}

