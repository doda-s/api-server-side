# To run the application in dev mode, use'fastapi dev main.py'
from fastapi import FastAPI

from api.controllers.home import router as home_router
from api.controllers.users import router as users_router
from api.controllers.auth import router as auth_router
from api.controllers.npcs import router as npcs_router
from api.controllers.achievements import router as achievement_router
from api.controllers.titles import router as titles_router

from api.database.database import DataBase

from api.models.user import User
from api.models.character import Character
from api.models.npc import Npc
from api.models.achievements import Achievements
from api.models.title import Title

app = FastAPI()

@app.on_event("startup")
async def startup():
    database = DataBase()
    database.MODELS = [
        User,
        Npc,
        Achievements,
        Title,
    ]
    await database.init()
    
    # Add the routes to application
    app.include_router(home_router)
    app.include_router(users_router)
    app.include_router(auth_router)
    app.include_router(npcs_router)
    app.include_router(achievement_router)
    app.include_router(titles_router)
