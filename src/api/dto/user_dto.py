from pydantic import BaseModel

from typing import Optional

from api.dto.character_dto import CharacterDto

# Modelo de user data transfer object
class UserDto(BaseModel):
    username: str
    character: Optional[CharacterDto] = None