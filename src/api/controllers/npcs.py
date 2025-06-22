from api.dto.character_dto import CharacterDto
from api.dto.user_dto import UserDto
from api.services import npcs
from api.middleware.authentication import token_required

from beanie.exceptions import DocumentNotFound

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from typing_extensions import Annotated

router = APIRouter()

@router.get("/npcs")
async def all_npcs():
    return await npcs.get_npcs_list()

@router.post("/npcs/create")
async def create_npc(
    character_dto: CharacterDto,
    current_user: Annotated[UserDto, Depends(token_required)]
):
    return await npcs.create_npc(current_user, character_dto)

@router.post("/npcs/update/{uuid}")
async def update_npc(
    current_user: Annotated[UserDto, Depends(token_required)],
    character_dto: CharacterDto,
    uuid: str
):
    try:
        return await npcs.update_npc(current_user, uuid, character_dto)
    except DocumentNotFound:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Não foi possível atualizar NPC.",
        )

@router.delete("/npcs/delete/{uuid}")
async def delete_npc(
    current_user: Annotated[UserDto, Depends(token_required)],
    uuid: str
):
    return await npcs.delete_npc(uuid)

@router.post("/npcs/select/{uuid}")
async def select_npc(
    uuid
):
    return await npcs.select_npc(uuid) 