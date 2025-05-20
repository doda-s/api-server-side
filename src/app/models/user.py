from beanie import Document, Link
from app.models.character import Character
from app.models.user_progress import UserProgress

class User(Document):
    username: str
    password: str
    character: Character
    user_progress: UserProgress