from fastapi.requests import Request
from typing import List, Optional

from aiofile import async_open

from uuid import uuid4

from sqlalchemy.future import select

from core.configs import settings
from core.database import get_session
from models.produto_model import ProdutoModel
from models.categoria_produto_model import CategoriaProdutoModel
from controllers.base_controller import BaseController

class ProdutoController(BaseController):

    def __init__(self, request: Request) -> None:
        super().__init__(request, ProdutoModel)

    async def get_categorias(self) -> Optional[List[CategoriaProdutoModel]]:
        """Retorna todas as categorias de produtos disponíveis"""
        async with get_session() as session:
            query = select(CategoriaProdutoModel)
            result = await session.execute(query)
            return result.scalars().all()
    
    async def get_categoria_produto(self, id: int) -> Optional[CategoriaProdutoModel]:
        """Retorna uma categoria de produto específica pelo ID"""
        async with get_session() as session:
            return await session.get(CategoriaProdutoModel, id)


    #Criar um novo produto
    async def post_crud(self) -> None:

        #Vai receber dados do formulario.
        form = await self.request.form()

        nome: str = form.get('nome')
        descricao: str = form.get('descricao')
        preco: float = form.get('preco')
        estoque: int = form.get('estoque')
        categoria_id: int = form.get('categoria_id')

        #Validação para que todos os campos sejam obrigatórios!
        if not nome or not descricao or not preco or not estoque or not categoria_id:
            raise ValueError("Todos os campos são obrigatórios.")

        #Instanciar o objeto
        produto: ProdutoModel = ProdutoModel(nome=nome, descricao=descricao, preco=preco, estoque=estoque, categoria_id=int(categoria_id))

        #Cria sessão e insere no banco
        async with get_session() as session:
            session.add(produto)
            await session.commit() 

        
    #Editar um produto
    async def put_crud(self, obj: object) -> None:
        async with get_session() as session:
            #Consultando se o produto existe no banco
            produto: ProdutoModel = await session.get(self.model, obj.id)

            if produto:
                #Recebe os dados do formulario
                form = await self.request.form()

                nome: str = form.get('nome')
                descricao: str = form.get('descricao')
                preco: float = form.get('preco')
                estoque: int = form.get('estoque')
                categoria_id: int = form.get('categoria_id')

                if nome and nome != produto.nome:
                    produto.nome = nome
                
                if descricao and descricao != produto.descricao:
                    produto.descricao = descricao

                if preco and preco != produto.preco:
                    produto.preco = preco

                if estoque and estoque != produto.estoque:
                    produto.estoque = estoque

                if categoria_id and categoria_id != produto.categoria_id:
                    produto.categoria_id = int(categoria_id)

                await session.commit()

        
        
