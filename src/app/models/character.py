from beanie import Document

class Character(Document):
    name: str
    age: int
    gender: str
    profession: str
    role: str