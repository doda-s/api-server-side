from beanie import Document, Indexed

from typing import Optional

from api.models.character import Character

# Modelo de usuário de exemplo
class User(Document):
    username: Indexed(str, unique=True)
    password: str
    character: Optional[Character] = None
    
    class Settings:
        name = "users"