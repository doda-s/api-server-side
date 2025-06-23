from pydantic import Field
from beanie import Document, Indexed
from uuid import uuid4, UUID

class Achievement(Document):
    id: UUID = Field(default_factory=uuid4)
    name: Indexed(str, unique=True) = Field(...)
    description: str = Field(...)
    
    class Settings:
        name = "achievements"