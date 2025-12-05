from fastapi.requests import Request

from datetime import datetime
from core.configs import settings
from core.database import get_session
from models.categoria_produto_model import CategoriaProdutoModel
from controllers.base_controller import BaseController

class CategoriaProdutoController(BaseController):

    def __init__(self, request: Request) -> None:
        super().__init__(request, CategoriaProdutoModel)

    #Criar Categoria de Produto
    async def post_crud(self) -> None:
        #Recebe dados do formulario
        form = await self.request.form()

        nome: str = form.get('nome')
        descricao: str = form.get('descricao')

        #Validação para que os campos nome e descricao sejam obrigatórios!
        if not nome or not descricao:
            raise ValueError("Todos os campos são obrigatórios.")

        #Instanciar objeto
        categoria_produto: CategoriaProdutoModel = CategoriaProdutoModel(nome=nome, descricao=descricao)
        
        #Cria a sessão e insere no banco
        async with get_session() as session:
            session.add(categoria_produto)
            await session.commit()

        
    #Edit de categoria de produto
    async def put_crud(self, obj: object) -> None:
        async with get_session() as session:
            #Consultando se a categoria existe no banco
            categoria_produto: CategoriaProdutoModel = await session.get(self.model, obj.id)

            if categoria_produto:
                #Recebe os dados do formulario
                form = await self.request.form()

                nome: str = form.get('nome')
                descricao: str = form.get('descricao')

                #O nome que recebemos é diferente do que está no banco?
                if nome and nome != categoria_produto.nome:
                    categoria_produto.nome = nome

                #O descricao que recebemos é diferente do que está no banco?
                if descricao and descricao != categoria_produto.descricao:
                    categoria_produto.descricao = descricao

                session.add(categoria_produto)
                await session.commit()

            