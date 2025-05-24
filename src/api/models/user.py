from beanie import Document, Indexed

# Modelo de usuário de exemplo
class User(Document):
    username: Indexed(str, unique=True)
    password: str
    
    class Settings:
        name = "users"