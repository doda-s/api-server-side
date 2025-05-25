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