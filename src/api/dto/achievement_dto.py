from pydantic import BaseModel

class AchievementDto(BaseModel):
    name: str
    description: str