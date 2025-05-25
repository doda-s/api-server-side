from beanie import Document, Indexed

# Modelo de usuário de exemplo
class Character(Document):
    name: str
    age: int
    gender: str
    profession: str
    role: str
    
    class Settings:
        name = "characters"