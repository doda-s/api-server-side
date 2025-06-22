from pydantic import BaseModel

class AchievementsDto(BaseModel):
    name: str
    description: str