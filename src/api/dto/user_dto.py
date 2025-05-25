from pydantic import BaseModel

# Modelo de user data transfer object
class UserDto(BaseModel):
    username: str