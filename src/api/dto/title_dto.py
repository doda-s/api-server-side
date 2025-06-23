from pydantic import BaseModel

from typing import Optional

from uuid import UUID

# Modelo de titulo
class TitleDto(BaseModel):
    id: Optional[UUID] = None
    title: str
    description: str