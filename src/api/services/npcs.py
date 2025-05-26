from api.dto.character_dto import CharacterDto
from api.dto.npc_dto import NpcDto
from api.models.npc import Npc
from api.models.character import Character

async def get_npcs_list():
    return await Npc.find_all().to_list()

async def create_npc(new_character: CharacterDto):
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

async def update_npc(uuid: str, new_character: CharacterDto):
    npc = await Npc.get(uuid)
    print(npc)
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

async def delete_npc(uuid):
    npc = await Npc.get(uuid)
    if not npc:
        return {"message": "NPC não encontrado."}
    await npc.delete()
    return {"message": "NPC deletado com sucesso!"}

async def select_npc(uuid):
    npc = await Npc.get(uuid)
    if not npc:
        return {"message": "NPC não encontrado."}
    return NpcDto(**npc.model_dump())