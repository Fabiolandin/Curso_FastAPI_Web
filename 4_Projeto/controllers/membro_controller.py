from fastapi.requests import Request
from fastapi import UploadFile

from aiofile import async_open

from uuid import uuid4

from core.configs import settings
from core.database import get_session
from models.membro_model import MembroModel
from controllers.base_controller import BaseController


class MembroController(BaseController):

    def __init__(self, request: Request) -> None:
        super().__init__(request, MembroModel)

    async def post_crud(self) -> None:
        #Vai receber dados do formulario
        form = await self.request.form()

        nome: str = form.get('nome')
        funcao: str = form.get('funcao')
        imagem: UploadFile = form.get('imagem')

        print("NOME:", nome)
        print("FUNCAO:", funcao)
        print("IMAGEM:", imagem)
        if not nome or not funcao or not imagem or not imagem.filename:
            raise ValueError("Todos os campos são obrigatórios.")
        
        #Nome aleatório para a imagem
        arquivo_ext: str = imagem.filename.split('.')[-1]
        novo_nome: str = f"{str(uuid4())}.{arquivo_ext}"

        #Instanciar o objeto
        membro: MembroModel = MembroModel(nome=nome, funcao=funcao, imagem=novo_nome)

        #Fazer o upload da imagem
        async with async_open(f"{settings.MEDIA}/{novo_nome}", 'wb') as afile:
            await afile.write(imagem.file.read())

        #Cria a sessão e insere no banco
        async with get_session() as session:
            session.add(membro)
            await session.commit()
    
    #Edit de membro
    async def put_crud(self, obj: object) -> None:
        async with get_session() as session:
            #Consultando se o membro existe no banco
            membro: MembroModel = await session.get(self.model, obj.id)

            if membro:
                #Recebe os dados do formulario
                form = await self.request.form()

                nome: str = form.get('nome')
                funcao: str = form.get('funcao')
                imagem: UploadFile = form.get('imagem')

                #O nome que recebemos do formulario é diferente do que está no banco?
                if nome and nome != membro.nome:
                    membro.nome = nome
                if funcao and funcao != membro.funcao:
                    membro.funcao = funcao
                if imagem.filename:
                    #Gera um nome aleatório para a imagem
                    arquivo_ext: str = imagem.filename.split('.')[-1]
                    novo_nome: str = f"{str(uuid4())}.{arquivo_ext}"
                    membro.imagem = novo_nome
                    #Faz o upload da imagem
                    async with async_open(f"{settings.MEDIA}/{novo_nome}", 'wb') as afile:
                        await afile.write(imagem.file.read())
                
                session.add(membro)
                await session.commit()