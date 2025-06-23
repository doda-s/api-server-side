from beanie import Document, Indexed

from typing import Optional, List

from pydantic import Field

from api.models.title import Title
from api.models.character import Character
from api.models.progress import Progress
from api.models.achievements import Achievements

from uuid import uuid4, UUID

from api.types.role_names import RoleNames

# Modelo de usuário de exemplo
class User(Document):
    id: UUID = Field(default_factory=uuid4)
    roles: list[RoleNames]
    username: Indexed(str, unique=True)
    password: str
    progress: Progress
    character: Optional[Character] = None
    achievements: list[str] = []
    titles: Optional[List[Title]] = Field(default_factory=list)

    class Settings:
        name = "users"