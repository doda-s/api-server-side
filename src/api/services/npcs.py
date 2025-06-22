from api.dto.character_dto import CharacterDto
from api.dto.npc_dto import NpcDto
from api.models.npc import Npc
from api.models.character import Character
from api.dto.user_dto import UserDto
from api.services.user import User
from api.types.role_names import RoleNames
from api.services.roles import check_if_has_role

from fastapi import status
from fastapi.exceptions import HTTPException

async def get_npcs_list():
    return await Npc.find_all().to_list()

async def create_npc(current_user: UserDto, new_character: CharacterDto):
    if await check_if_has_role(current_user, RoleNames.ADMIN):
        character = Character(
            name=new_character.name,
            age=new_character.age,
            gender=new_character.gender,
            profession=new_character.profession,
            role=new_character.role
        )
        new_npc = Npc(character=character)
        await new_npc.save()
        return NpcDto(**new_npc.model_dump())
    
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não autorizado!"
        )

async def update_npc(
    current_user: UserDto,
    uuid: str,
    new_character: CharacterDto
):
    if await check_if_has_role(current_user, RoleNames.ADMIN):
        npc = await Npc.get(uuid)
        if not npc:
            return
        character = Character(
            name=new_character.name,
            age=new_character.age,
            gender=new_character.gender,
            profession=new_character.profession,
            role=new_character.role
        )
        npc.character = character
        await npc.replace()
        return NpcDto(**npc.model_dump())

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Usuário não autorizado!"
    )

async def delete_npc(current_user: UserDto, uuid):
    if await check_if_has_role(current_user, RoleNames.ADMIN):
        npc = await Npc.get(uuid)
        if not npc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="NPC não encontrado."
            )
        await npc.delete()
        return {"message": "NPC deletado com sucesso!"}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Usuário não autorizado!"
    )

async def select_npc(uuid):
    npc = await Npc.get(uuid)
    if not npc:
        return {"message": "NPC não encontrado."}
    return NpcDto(**npc.model_dump())