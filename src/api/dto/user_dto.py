from pydantic import BaseModel

from typing import Optional

from api.dto.character_dto import CharacterDto
from api.dto.progress_dto import ProgressDto

from uuid import UUID

# Modelo de user data transfer object
class UserDto(BaseModel):
    id: UUID
    username: str
    progress: ProgressDto
    character: Optional[CharacterDto] = None