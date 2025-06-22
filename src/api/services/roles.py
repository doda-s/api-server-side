from api.dto.user_dto import UserDto
from api.types.role_names import RoleNames
from api.models.user import User

from fastapi.exceptions import HTTPException
from fastapi import status

async def check_if_has_role(current_user: UserDto, role:RoleNames)->bool:
    user = await User.get(current_user.id)
    if not user:
        return False
        
    if not RoleNames.ADMIN in user.roles:
        return False
    
    return True