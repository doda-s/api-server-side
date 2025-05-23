from beanie import Document

# Modelo de usuário de exemplo
class User(Document):
    username: str
    password: str
    
    class Settings:
        name = "users"