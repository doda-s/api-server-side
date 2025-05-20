from flask import Blueprint

routes_blueprint = Blueprint('main', __name__)

# Encapsular rotas
from app.routes import users