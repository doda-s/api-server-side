from fastapi import Depends, status

from fastapi.exceptions import HTTPException

from api.types.role_names import RoleNames
from api.dto.user_dto import UserDto
from api.dto.title_dto import TitleDto
from api.models.title import Title
from api.services.roles import check_if_has_role

from typing_extensions import Annotated

async def add_title(current_user: UserDto, title_dto: TitleDto):
    if not await check_if_has_role(current_user, RoleNames.ADMIN):
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Sem permissão!"
            )
    new_title = Title(
        title = title_dto.title,
        description = title_dto.description
    )
    
    try:
        await new_title.insert()
        return {"message": "Título foi adicionado com sucesso!"}
    except :
        return {"message": "Não foi possível criar o título!"}
    
async def get_all_titles(current_user: UserDto):
    titles = await Title.find_all().to_list()
    return titles

async def get_title_by_id(current_user: UserDto, id):
    if not validate_title(id): raise HTTPException(status_code=404, detail="Título não encontrado")
    title = await Title.get(id)
    return TitleDto(**title.model_dump())

async def validate_title(id)->bool:
    try:
        title = await Title.get(id)
    except:
        return False
    return True

async def get_user_titles_name_description(current_user: UserDto, titles: list):
    titles_data = []
    for title in titles:
        try:
            result = await get_title_by_id(current_user, title)
        except:
            continue
        titles_data.append({
            "title": result.title,
            "description": result.description
            })
    return titles_data