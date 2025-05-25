import jwt
from jwt.exceptions import InvalidTokenError

from fastapi import status, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext

from api.dto.user_dto import UserDto
from api.dto.token import TokenData
from api.services.user import get_user

from datetime import timedelta, datetime, timezone

from config import Config

from typing_extensions import Annotated


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

# Compara dois hashs de senha
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Encripta uma senha em um hash
def get_password_hash(password):
    return pwd_context.hash(password)

# Gera um JWT access_token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        Config.SECRET_KEY,
        Config.ALGORITHM
    )
    return encoded_jwt

# Busca no banco de dados um usuário com o mesmo username passado no parâmetro.
# Depois compara se os hashs de senha são os mesmos.
async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    
    return user

# Retorna um user baseado no token passado como parâmetro
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]): # get_current_user
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar credenciais.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            Config.SECRET_KEY,
            algorithms=Config.ALGORITHM
        )
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user