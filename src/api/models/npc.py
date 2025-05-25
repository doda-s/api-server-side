from api.models.character import Character

from beanie import Document

from pydantic import Field

from uuid import uuid4, UUID

class Npc(Document):
    id: UUID = Field(default_factory=uuid4)
    character: Character
    
    class Settings:
        name = "npcs"