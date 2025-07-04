# To run the application in dev mode, use'fastapi dev main.py'
from fastapi import FastAPI

from api.controllers.home import router as home_router
from api.controllers.users import router as users_router
from api.controllers.auth import router as auth_router
from api.controllers.npcs import router as npcs_router

from api.database.database import DataBase

from api.models.user import User
from api.models.character import Character
from api.models.npc import Npc

app = FastAPI()

@app.on_event("startup")
async def startup():
    database = DataBase()
    database.MODELS = [
        User,
        Npc,
    ]
    await database.init()
    
    # Add the routes to application
    app.include_router(home_router)
    app.include_router(users_router)
    app.include_router(auth_router)
    app.include_router(npcs_router)