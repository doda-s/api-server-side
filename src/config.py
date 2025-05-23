import os

# Caminho relativo para a aplicação
application_absolute_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    
    # Busca um arquivo na estrutura de arquivos contendo a chave secreta
    # Utilizamos 'you-will-never-guess' para ambiente de desenvolvimento
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess.'
    
    # Endereço para o banco de dados
    MONGODB_DATABASE_URI = 'mongodb://localhost:27017'
    DATABASE_NAME = "server-side-api"