from typing import Optional, List

from fastapi.requests import Request
from sqlalchemy.future import select

from core.database import get_session

class BaseController:

    def __init__(self, request: Request, model: object) -> None:
        self.request = request
        self.model = model

    async def get_all_crud(self) -> Optional[List[object]]:
        """ Método genérico para retornar todos os objetos do model """
        async with get_session() as session:
            query = select(self.model)
            result = await session.execute(query)

            return result.scalars().all()
        
    async def get_one_crud(self, id_obj: int) -> Optional[object]:
        """ Método genérico para retornar um objeto pelo ID """
        async with get_session() as session:
            obj = self.model = await session.get(self.model, id_obj)
            return obj
            
    async def post_crud(self) -> None:
        """ Não é um metodo genérico, deve ser implementado na subclasse """
        raise NotImplementedError("Método post_crud não implementado")
    
    async def put_crud(self) -> None:
        """ Não é um metodo genérico, deve ser implementado na subclasse """
        raise NotImplementedError("Método put_crud não implementado")
    
    async def delete_crud(self, id_obj: int) -> None:
        """ Método genérico para deletar um objeto pelo ID """
        async with get_session() as session:
            obj: self.model = await session.get(self.model, id_obj)
            if obj:
                await session.delete(obj)
                await session.commit()

