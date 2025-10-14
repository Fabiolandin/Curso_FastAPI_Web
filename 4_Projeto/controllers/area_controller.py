from fastapi.requests import Request

from aiofile import async_open

from core.configs import settings
from core.database import get_session
from models.area_model import AreaModel
from controllers.base_controller import BaseController

class AreaController(BaseController):

    def __init__(self, request: Request) -> None:
        super().__init__(request, AreaModel)

    #Criar uma nova área
    async def post_crud(self) -> None:

        #Recebe dados do formulario
        form = await self.request.form()

        area: str = form.get('area')

        #Validação para que todos os campos sejam obrigatórios!
        if not area:
            raise ValueError("O campo área é obrigatório.")
        
        #Instanciar o objeto
        area: AreaModel = AreaModel(area=area)

        #Cria a sessão e insere no banco
        async with get_session() as session:
            session.add(area)
            await session.commit()

        
    #Editar uma área
    async def put_crud(self, obj: object) -> None:
        async with get_session() as session:
            #Consultando se a área existe no banco
            area: AreaModel = await session.get(self.model, obj.id)

            if area:
                #Recebe os dados do formulario
                form = await self.request.form()

                nova_area: str = form.get('area')

                #Validação para que todos os campos sejam obrigatórios!
                if not nova_area:
                    raise ValueError("O campo área é obrigatório.")
                
                area.area = nova_area

                await session.commit()
            else:
                raise ValueError("Área não encontrada.")