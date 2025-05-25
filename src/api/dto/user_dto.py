from pydantic import BaseModel

from typing import Optional

from api.dto.character_dto import CharacterDto

from uuid import UUID

# Modelo de user data transfer object
class UserDto(BaseModel):
    id: UUID
    username: str
    character: Optional[CharacterDto] = None