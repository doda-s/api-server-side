from pydantic import BaseModel

class CharacterDto(BaseModel):
    name: str
    age: int
    gender: str
    profession: str
    role: str