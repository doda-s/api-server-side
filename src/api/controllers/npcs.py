from api.dto.character_dto import CharacterDto
from api.services import npcs

from beanie.exceptions import DocumentNotFound

from fastapi import APIRouter
from fastapi.exceptions import HTTPException

router = APIRouter()

@router.get("/npcs")
async def all_npcs():
    return await npcs.get_npcs_list()

@router.post("/npcs/create")
async def create_npc(
    character_dto: CharacterDto
):
    return await npcs.create_npc(character_dto)

@router.post("/npcs/update/{uuid}")
async def update_npc(
    character_dto: CharacterDto,
    uuid: str
):
    try:
        return await npcs.update_npc(uuid, character_dto)
    except DocumentNotFound:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Não foi possível atualizar NPC.",
        )