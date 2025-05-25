from pydantic import BaseModel

# Modelo de usuário de exemplo
class Character(BaseModel):
    name: str
    age: int
    gender: str
    profession: str
    role: str