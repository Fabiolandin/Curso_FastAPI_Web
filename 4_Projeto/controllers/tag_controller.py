from fastapi.requests import Request

from aiofile import async_open

from core.configs import settings
from core.database import get_session
from models.tag_model import TagModel
from controllers.base_controller import BaseController

class TagController(BaseController):

    def __init__(self, request: Request) -> None:
        super().__init__(request, TagModel)

    #Criar uma nova tag
    async def post_crud(self) -> None:

        #Recebe dados do formulario
        form = await self.request.form()

        tag: str = form.get('tag')

        #Validação para que todos os campos sejam obrigatórios!
        if not tag:
            raise ValueError("O campo tag é obrigatório.")
        
        #Instanciar o objeto
        tag: TagModel = TagModel(tag=tag)

        #Cria a sessão e insere no banco
        async with get_session() as session:
            session.add(tag)
            await session.commit()

    
    #Editar uma tag
    async def put_crud(self, obj: object) -> None:
        async with get_session() as session:
            #Consultando se a tag existe no banco
            tag: TagModel = await session.get(self.model, obj.id)

            if tag:
                #Recebe os dados do formulario
                form = await self.request.form()

                nova_tag: str = form.get('tag')

                #Validação para que todos os campos sejam obrigatórios!
                if not nova_tag:
                    raise ValueError("O campo tag é obrigatório.")
                
                tag.tag = nova_tag

                await session.commit()
            else:
                raise ValueError("Tag não encontrada.")