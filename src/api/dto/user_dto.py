from pydantic import BaseModel

from typing import Optional, List

from api.dto.title_dto import TitleDto
from api.dto.character_dto import CharacterDto
from api.dto.progress_dto import ProgressDto

from uuid import UUID

# Modelo de user data transfer object
class UserDto(BaseModel):
    id: UUID
    username: str
    progress: ProgressDto
    character: Optional[CharacterDto] = None
    achievements: list[str] = []
    titles: list[str] = []