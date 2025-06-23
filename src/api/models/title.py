from beanie import Document, Indexed

from pydantic import Field

from uuid import uuid4, UUID

from api.types.role_names import RoleNames

# Modelo de usuário de exemplo
class Title(Document):
    id: UUID = Field(default_factory=uuid4)
    title: str
    description:  str
    
    class Settings:
        name: "titles"