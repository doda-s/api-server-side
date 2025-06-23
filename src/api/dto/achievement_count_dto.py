from pydantic import BaseModel

class AchievementCountDto(BaseModel):
    id: str
    achievement_name: str
    achievement_desciption: str
    global_count: int