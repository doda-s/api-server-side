import asyncio

from flask import Flask
from config import Config

from app.database.database import DataBase

from app.models.user import User
from app.models.character import Character

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Database setup
    data_base = DataBase()
    data_base.MODELS = [
        User,
        Character,
    ]
    asyncio.run(data_base.init())
    
    return app