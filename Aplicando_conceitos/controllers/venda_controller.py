from datetime import datetime
from fastapi.requests import Request
from typing import List, Optional

from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from core.configs import settings
from core.database import get_session
from models.venda_model import VendaModel
from models.fornecedor_model import FornecedorModel
from models.funcionario_model import FuncionarioModel
from controllers.base_controller import BaseController
from models.produto_model import ProdutoModel
from models.item_venda_model import ItemVendaModel

class VendaController(BaseController):

    def __init__(self, request: Request) -> None:
        super().__init__(request, VendaModel)

    async def get_all_crud(self) -> Optional[List[VendaModel]]:
        async with get_session() as session:
            query = select(VendaModel).options(joinedload(VendaModel.fornecedor), joinedload(VendaModel.funcionario), joinedload(VendaModel.item_venda))
            result = await session.execute(query)
            return result.unique().scalars().all()
    
    async def get_one_crud(self, id_obj: int) -> Optional[VendaModel]:
        async with get_session() as session:
            query = select(VendaModel).options(joinedload(VendaModel.fornecedor), joinedload(VendaModel.funcionario), joinedload(VendaModel.item_venda).joinedload(ItemVendaModel.produto)).filter(VendaModel.id == id_obj)
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

    async def get_itens_venda(self) -> Optional[List[ItemVendaModel]]:
        async with get_session() as session:
            query = select(ItemVendaModel)
            result = await session.execute(query)
            return result.scalars().all()

    #Criar Venda
    async def post_crud(self) -> None:
        #Vai receber dados do formulario
        form = await self.request.form()

        fornecedor_id: int = int(form.get('fornecedor_id'))
        funcionario_id: int = int(form.get('funcionario_id'))
        data_venda_str: str = form.get('data_venda')
        
        # Listas dinamicas do Formulario
        produto_ids = form.getlist('produto_id')
        quantidades = form.getlist('quantidade')
        precos_unitarios = form.getlist('valor_unitario')

        #Validação básica para adicionar fornecedor funcionario e data
        if not fornecedor_id or not funcionario_id or not data_venda_str:
             raise ValueError("Campos obrigatórios: Fornecedor, Funcionário e Data.")
        
        #Validação básica para adicionar produto quantidade e preco unitario
        if not produto_ids or not quantidades or not precos_unitarios:
             raise ValueError("Adicione pelo menos um produto à venda.")

        async with get_session() as session:
            venda: VendaModel = VendaModel(
                fornecedor_id=fornecedor_id, 
                funcionario_id=funcionario_id, 
                data_venda=datetime.strptime(data_venda_str, '%Y-%m-%d') if data_venda_str else datetime.now(),
                valor_total=0.0
            )
            session.add(venda)
            await session.flush()

            valor_total_acumulado = 0.0

            #Iterando itens das listas
            for p_id, qtd, preco in zip(produto_ids, quantidades, precos_unitarios):
                p_id = int(p_id)
                qtd = int(qtd)
                preco = float(preco.replace(',', '.'))

                #Cria item
                item = ItemVendaModel(
                    venda_id=venda.id,
                    produto_id=p_id,
                    quantidade=qtd,
                    preco_unitario=preco
                )
                session.add(item)

                #Atualiza estoque
                produto = await session.get(ProdutoModel, p_id)
                if produto:
                    produto.estoque -= qtd
                    session.add(produto)
                
                valor_total_acumulado += (qtd * preco)

            #Atualiza valor total de venda
            venda.valor_total = valor_total_acumulado
            session.add(venda)

            await session.commit()

    #Editar uma venda
    async def put_crud(self, obj: object) -> None:
        async with get_session() as session:
            #Consultando se a venda existe no banco
            venda: VendaModel = await session.get(VendaModel, obj.id)

            if venda:
                #Recebe os dados do form
                form = await self.request.form()

                fornecedor_id: int = int(form.get('fornecedor_id'))
                funcionario_id: int = int(form.get('funcionario_id'))
                data_venda: str = form.get('data_venda')
                valor_total: float = float(form.get('valor_total').replace(',', '.'))
                
                if fornecedor_id and fornecedor_id != venda.fornecedor_id:
                    venda.fornecedor_id = int(fornecedor_id)

                if funcionario_id and funcionario_id != venda.funcionario_id:
                    venda.funcionario_id = int(funcionario_id)

                if data_venda and data_venda != venda.data_venda:
                    venda.data_venda = data_venda

                if valor_total and valor_total != venda.valor_total:
                    venda.valor_total = valor_total

                await session.commit()
    
    async def delete_crud(self, id_obj: int) -> None:
        async with get_session() as session:
            #Faz o Select da compra e dos itens:
            query = select(VendaModel).options(joinedload(VendaModel.item_venda)).filter(VendaModel.id == id_obj)
            result = await session.execute(query)
            venda = result.unique().scalars().first()

            if venda:
                #Reverte o estoque
                for item in venda.item_venda:
                     # Busca o produto para garantir que ele esteja na sessão atual
                     produto = await session.get(ProdutoModel, item.produto_id)
                     if produto:
                         produto.estoque += item.quantidade
                         session.add(produto)
                
                #Deleta os itens
                for item in venda.item_venda:
                    await session.delete(item)
                
                #Deleta a venda
                await session.delete(venda)
                await session.commit()
