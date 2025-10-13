from fastapi.requests import Request
from fastapi import UploadFile

from aiofile import async_open

from uuid import uuid4

from core.configs import settings
from core.database import get_session
from models.autor_model import AutorModel
from controllers.base_controller import BaseController

class AutorController(BaseController):

    def __init__(self, request: Request) -> None:
        super().__init__(request, AutorModel)

    #Criar um novo autor
    async def post_crud(self) -> None:

        #Vai receber dados do formulario.
        form = await self.request.form()

        nome: str = form.get('nome')
        imagem: UploadFile = form.get('imagem')

        #Validação para que todos os campos sejam obrigatórios!
        if not nome or not imagem or not imagem.filename:
            raise ValueError("Todos os campos são obrigatórios.")
        
        #Gerando nome aleatório para a imagem
        arquivo_ext: str = imagem.filename.split('.')[-1]
        novo_nome: str = f"{str(uuid4())}.{arquivo_ext}"

        #Instanciar o objeto
        autor: AutorModel = AutorModel(nome=nome, imagem=novo_nome)

        #Fazer o upload da imagem
        async with async_open(f"{settings.MEDIA}/{novo_nome}", 'wb') as afile:
            await afile.write(imagem.file.read())

        #Cria a sessão e insere no banco
        async with get_session() as session:
            session.add(autor)
            await session.commit()

    
    #Editar um autor
    async def put_crud(self, obj: object) -> None:
        async with get_session() as session:
            #Consultando se o autor existe no banco
            autor: AutorModel = await session.get(self.model, obj.id)

            if autor:
                #Recebe os dados do formulario
                form = await self.request.form()

                nome: str = form.get('nome')
                imagem: UploadFile = form.get('imagem')

                #Atualiza o nome
                autor.nome = nome

                #Verifica se uma nova imagem foi enviada
                if imagem and imagem.filename:
                    #Gerando nome aleatório para a imagem
                    arquivo_ext: str = imagem.filename.split('.')[-1]
                    novo_nome: str = f"{str(uuid4())}.{arquivo_ext}"

                    #Fazer o upload da nova imagem
                    async with async_open(f"{settings.MEDIA}/{novo_nome}", 'wb') as afile:
                        await afile.write(imagem.file.read())
                    
                    #Atualiza o nome da imagem no banco
                    autor.imagem = novo_nome
                
                #Faz o commit no banco de dados
                session.add(autor)
                await session.commit()
