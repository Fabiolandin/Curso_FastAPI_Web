from typing import Optional, List

from fastapi.requests import Request
from sqlalchemy.future import select

from core.database import get_session
from models.tag_model import TagModel
from models.autor_model import AutorModel
from models.post_model import PostModel

class BaseController:

    def __init__(self, request: Request, model: object) -> None:
        self.request: Request = request
        self.model: object = model
    
    async def get_all_crud(self) -> Optional[List[object]]:
        """ Retorna todos os registros do Model """
        async with get_session() as session:
            query = select(self.model)
            result = await session.execute(query)

            return result.unique().scalars().all()
        
    async def get_one_crud(self, id_obj: int) -> Optional[object]:
        """ Retorna o objeto especificado pelo id ou None """
        async with get_session() as session:
            obj: self.model = await session.get(self.model, id_obj)
            return obj
        
    async def post_crud(self) -> None:
        raise NotImplementedError("Método post_crud não implementado")
    
    async def put_crud(self, obj: object) -> None:
        raise NotImplementedError("Método put_crud não implementado")
    
    async def delete_crud(self, id_obj: int) -> None:
        """ Deleta o objeto especificado pelo id """
        async with get_session() as session:
            obj: self.model = await session.get(self.model, id_obj)
            if obj:
                await session.delete(obj)
                await session.commit()

    
    #Buscar todas as tags
    async def get_tags(self) -> Optional[List[TagModel]]:
        """ Retorna todos os registros de tag """
        async with get_session() as session:
            query = select(TagModel)
            result = await session.execute(query)
            tags: Optional[List[TagModel]] = result.scalars().unique().all()

            return tags
        
    #Buscar uma tag pelo id
    async def get_tag(self, id_tag: int) -> TagModel:
        """ Retorna uma tag pelo id_obj ou None"""
        async with get_session() as session:
            tag: TagModel = await session.get(TagModel, id_tag)
            
        return tag

