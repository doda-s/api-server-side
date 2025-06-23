from pydantic import BaseModel

class AchievementPercentageDto(BaseModel):
    id: str
    achievement_name: str
    achievement_desciption: str
    global_percentage: float