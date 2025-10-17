from fastapi.requests import Request
from fastapi import UploadFile
from typing import List, Optional

from aiofile import async_open

from uuid import uuid4

from core.configs import settings
from core.database import get_session
from models.autor_model import AutorModel
from models.tag_model import TagModel
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
        tags: List[str] = form.getlist('tag')

        #Validação para que todos os campos sejam obrigatórios!
        if not nome or not imagem or not imagem.filename:
            raise ValueError("Todos os campos são obrigatórios.")
        
        #Gerando nome aleatório para a imagem
        arquivo_ext: str = imagem.filename.split('.')[-1]
        novo_nome: str = f"{str(uuid4())}.{arquivo_ext}"

        #Instanciar o objeto
        autor: AutorModel = AutorModel(nome=nome, imagem=novo_nome)

        #Busca e adiciona as tags
        for id_tag in tags:
            tag = await self.get_tag(id_tag=int(id_tag))
            autor.tags.append(tag)

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
                tags: List[str] = form.getlist('tag')

                if nome and nome != autor.nome:
                    autor.nome = nome


                #Limpa as tags atuais
                autor.tags = []

                # Adiciona apenas as selecionadas (se houver)
                for id_tag in tags:
                    tag = await self.get_tag(int(id_tag))
                    tag_local = await session.merge(tag)
                    autor.tags.append(tag_local)

                if imagem.filename:
                    # Gera um nome aleatório
                    arquivo_ext: str = imagem.filename.split('.')[-1]
                    novo_nome: str = f"{str(uuid4())}.{arquivo_ext}"
                    autor.imagem = novo_nome
                    # Faz o upload da imagem
                    async with async_open(f"{settings.MEDIA}/autor/{novo_nome}", "wb") as afile:
                        await afile.write(imagem.file.read())
                await session.commit()
