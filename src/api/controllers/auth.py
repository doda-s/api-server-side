from fastapi import APIRouter

from api.services.user import create_user
from api.dto.user_auth_dto import UserAuthDto

router = APIRouter()

@router.post("/auth/register")
async def register_user(user_auth_dto: UserAuthDto):
    return await create_user(user_auth_dto=user_auth_dto)