from fastapi import APIRouter

from api.services import global_stats as global_stats_service

router = APIRouter()

@router.get("/stats/global")
async def get_global_stats(metric:str="count"):
    if metric == "percentage":
        return await global_stats_service.get_achievements_global_percentage()
    
    return await global_stats_service.get_achievements_global_count()