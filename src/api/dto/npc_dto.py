from api.models.character import Character
from pydantic import BaseModel
from uuid import UUID

class NpcDto(BaseModel):
    id: UUID
    character: Character