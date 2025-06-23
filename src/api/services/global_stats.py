from api.models.achievements import Achievements
from api.models.user import User
from api.dto.achievement_count_dto import AchievementCountDto
from api.dto.achievement_percentage_dto import AchievementPercentageDto

from beanie.odm.operators.find.comparison import NE

async def get_achievements_global_percentage():
    global_achievements_count = await get_global_achievements_stats_count()
    all_users_list = await User.find(NE(User.character, None)).to_list()
    all_users_count = len(all_users_list)
    achievement_stat_dto_list: list[AchievementStatDto] = []
    percentage = 0
    
    for achievement in global_achievements_count:
        if not all_users_count == 0:
            percentage = (achievement["global_count"] / all_users_count) * 100

        achievement_stat_dto_list.append(
            AchievementPercentageDto(
                id=achievement["id"],
                achievement_name=achievement["achievement_name"],
                achievement_desciption=achievement["achievement_desciption"],
                global_percentage=percentage
            )
        )
        
    return achievement_stat_dto_list

async def get_achievements_global_count():
    global_achievements_count = await get_global_achievements_stats_count()
    achievement_stat_dto_list: list[AchievementStatDto] = []
    
    for achievement in global_achievements_count:
        achievement_stat_dto_list.append(
            AchievementCountDto(
                id=achievement["id"],
                achievement_name=achievement["achievement_name"],
                achievement_desciption=achievement["achievement_desciption"],
                global_count=achievement["global_count"]
            )
        )
        
    return achievement_stat_dto_list

async def get_global_achievements_stats_count():
    all_achievements = await Achievements.find_all().to_list()
    achievements_ids = [a.id for a in all_achievements]
    achievements_count = await get_chievements_count_by_user()
    achievement_stat_dto_list = []
    
    for achievement in all_achievements:
        if not any(a["_id"] == str(achievement.id) for a in achievements_count):
            achievement_stat_dto_list.append(
                {
                    "id": str(achievement.id),
                    "achievement_name": achievement.name,
                    "achievement_desciption": achievement.description,
                    "global_count": 0
                }
            )
            continue
        
        count = next(
            (a for a in achievements_count if a["_id"] == str(achievement.id)),
            None
        )
        achievement_stat_dto_list.append(
            {
                "id": str(achievement.id),
                "achievement_name": achievement.name,
                "achievement_desciption": achievement.description,
                "global_count": count["count"]
            }
        )
    
    return achievement_stat_dto_list

async def get_chievements_count_by_user():
    pipeline = [
        {"$unwind": "$achievements"},
        {"$group": {"_id": "$achievements", "count": {"$sum": 1}}},
    ]
    stats = await User.get_motor_collection().aggregate(pipeline).to_list(length=None)
    
    return stats