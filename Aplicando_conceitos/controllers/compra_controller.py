from datetime import datetime
from fastapi.requests import Request
from typing import List, Optional

from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from core.configs import settings
from core.database import get_session
from models.compra_model import CompraModel
from models.fornecedor_model import FornecedorModel
from models.funcionario_model import FuncionarioModel
from controllers.base_controller import BaseController
from models.produto_model import ProdutoModel
from models.item_compra_model import ItemCompraModel

class CompraController(BaseController):

    def __init__(self, request: Request) -> None:
        super().__init__(request, CompraModel)

    async def get_all_crud(self) -> Optional[List[CompraModel]]:
        async with get_session() as session:
            query = select(CompraModel).options(joinedload(CompraModel.fornecedor), joinedload(CompraModel.funcionario), joinedload(CompraModel.item_compra))
            result = await session.execute(query)
            return result.unique().scalars().all()

    async def get_one_crud(self, id_obj: int) -> Optional[CompraModel]:
        async with get_session() as session:
            query = select(CompraModel).options(joinedload(CompraModel.fornecedor), joinedload(CompraModel.funcionario), joinedload(CompraModel.item_compra).joinedload(ItemCompraModel.produto)).filter(CompraModel.id == id_obj)
            result = await session.execute(query)
            return result.unique().scalars().first()

    async def get_fornecedores(self) -> Optional[List[FornecedorModel]]:
        async with get_session() as session:
            query = select(FornecedorModel)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_funcionarios(self) -> Optional[List[FuncionarioModel]]:
        async with get_session() as session:
            query = select(FuncionarioModel)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_produtos(self) -> Optional[List[ProdutoModel]]:
        async with get_session() as session:
            query = select(ProdutoModel)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_itens_compra(self) -> Optional[List[ItemCompraModel]]:
        async with get_session() as session:
            query = select(ItemCompraModel)
            result = await session.execute(query)
            return result.scalars().all()

    #Criar uma compra
    async def post_crud(self) -> None:
        #Vai receber dados do formulario
        form = await self.request.form()

        fornecedor_id: int = int(form.get('fornecedor_id'))
        funcionario_id: int = int(form.get('funcionario_id'))
        data_compra_str: str = form.get('data_compra')
        
        # Listas dinamicas do Formulario
        produto_ids = form.getlist('produto_id')
        quantidades = form.getlist('quantidade')
        precos_unitarios = form.getlist('valor_unitario')

        #Validação básica para adicionar fornecedor funcionario e data
        if not fornecedor_id or not funcionario_id or not data_compra_str:
             raise ValueError("Campos obrigatórios: Fornecedor, Funcionário e Data.")
        
        #Validação básica para adicionar produto quantidade e preco unitario
        if not produto_ids or not quantidades or not precos_unitarios:
             raise ValueError("Adicione pelo menos um produto à compra.")

        async with get_session() as session:
            compra: CompraModel = CompraModel(
                fornecedor_id=fornecedor_id, 
                funcionario_id=funcionario_id, 
                data_compra=datetime.strptime(data_compra_str, '%Y-%m-%d') if data_compra_str else datetime.now(),
                valor_total=0.0
            )
            session.add(compra)
            await session.flush()

            valor_total_acumulado = 0.0

            #Iterando itens das listas
            for p_id, qtd, preco in zip(produto_ids, quantidades, precos_unitarios):
                p_id = int(p_id)
                qtd = int(qtd)
                preco = float(preco.replace(',', '.'))

                #Cria item
                item = ItemCompraModel(
                    compra_id=compra.id,
                    produto_id=p_id,
                    quantidade=qtd,
                    preco_unitario=preco
                )
                session.add(item)

                #Atualiza estoque
                produto = await session.get(ProdutoModel, p_id)
                if produto:
                    produto.estoque += qtd
                    session.add(produto)
                
                valor_total_acumulado += (qtd * preco)

            #Atualiza valor total de compra
            compra.valor_total = valor_total_acumulado
            session.add(compra)

            await session.commit()

    #Editar uma compra
    async def put_crud(self, obj: object) -> None:
        async with get_session() as session:
            #Consultando se a compra existe no banco
            compra: CompraModel = await session.get(self.model, obj.id)

            if compra:
                #Recebe os dados do formulario
                form = await self.request.form()

                fornecedor_id: int = form.get('fornecedor_id')
                funcionario_id: int = form.get('funcionario_id')
                data_compra: datetime = form.get('data_compra')
                valor_total: float = form.get('valor_total')

                if fornecedor_id and fornecedor_id != compra.fornecedor_id:
                    compra.fornecedor_id = int(fornecedor_id)

                if funcionario_id and funcionario_id != compra.funcionario_id:
                    compra.funcionario_id = int(funcionario_id)

                if data_compra and data_compra != compra.data_compra:
                    compra.data_compra = data_compra

                if valor_total and valor_total != compra.valor_total:
                    compra.valor_total = valor_total

                await session.commit()

    async def delete_crud(self, id_obj: int) -> None:
        async with get_session() as session:
            #Faz o Select da compra e dos itens:
            query = select(CompraModel).options(joinedload(CompraModel.item_compra)).filter(CompraModel.id == id_obj)
            result = await session.execute(query)
            compra = result.unique().scalars().first()

            if compra:
                #Reverte o estoque
                for item in compra.item_compra:
                     # Busca o produto para garantir que ele esteja na sessão atual
                     produto = await session.get(ProdutoModel, item.produto_id)
                     if produto:
                         produto.estoque -= item.quantidade
                         session.add(produto)
                
                #Deleta os itens
                for item in compra.item_compra:
                    await session.delete(item)
                
                #Deleta a compra
                await session.delete(compra)
                await session.commit()