# To run the application in dev mode, use'fastapi dev main.py'
from fastapi import FastAPI

from api.controllers import home
from api.controllers import users
from api.controllers import auth

from api.database.database import DataBase

from api.models.user import User
from api.models.character import Character

app = FastAPI()

@app.on_event("startup")
async def startup():
    database = DataBase()
    database.MODELS = [
        User,
        Character,
    ]
    await database.init()
    
    # Add the routes to application
    app.include_router(home.router)
    app.include_router(users.router)
    app.include_router(auth.router)