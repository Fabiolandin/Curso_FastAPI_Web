from fastapi.requests import Request
from typing import List, Optional

from aiofile import async_open

from uuid import uuid4

from core.configs import settings
from core.database import get_session
from models.produto_model import ProdutoModel
from controllers.base_controller import BaseController

class ProdutoController(BaseController):

    def __init__(self, request: Request) -> None:
        super().__init__(request, ProdutoModel)

    #Criar um novo produto
    async def post_crud(self) -> None:

        #Vai receber dados do formulario.
        form = await self.request.form()

        nome: str = form.get('nome')
        descricao: str = form.get('descricao')
        preco: float = form.get('preco')
        estoque: int = form.get('estoque')
        categoria_produtos: List[str] = form.getlist('categoria_produto')

        #Validação para que todos os campos sejam obrigatórios!
        if not nome or not descricao or not preco or not estoque or not categoria_produtos:
            raise ValueError("Todos os campos são obrigatórios.")

        #Instanciar o objeto
        produto: ProdutoModel = ProdutoModel(nome=nome, descricao=descricao, preco=preco, estoque=estoque)

        #Buscar as categorias
        for id in categoria_produtos:
            categoria_produto = await self.get_categoria_produto(id=int(id))
            produto.categorias.append(categoria_produto)

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
                categoria_produtos: List[str] = form.getlist('categoria_produto')

                if nome and nome != produto.nome:
                    produto.nome = nome

                #Limpa as categorias atuais
                produto.categorias = []

                #Buscar as categorias e adiciona ao produto
                for id in categoria_produtos:
                    categoria_produto = await self.get_categoria_produto(id=int(id))
                    produto.categorias.append(categoria_produto)

                await session.commit()

        
        
