from datetime import datetime
from fastapi.requests import Request
from typing import List, Optional

from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from core.configs import settings
from core.database import get_session
from models.pedido_model import PedidoModel
from models.cliente_model import ClienteModel
from models.funcionario_model import FuncionarioModel
from models.produto_model import ProdutoModel
from models.item_pedido_model import ItemPedidoModel
from controllers.base_controller import BaseController

class PedidoController(BaseController):

    def __init__(self, request: Request) -> None:
        super().__init__(request, PedidoModel)

    async def get_all_crud(self) -> Optional[List[PedidoModel]]:
        async with get_session() as session:
            query = select(PedidoModel).options(joinedload(PedidoModel.cliente), joinedload(PedidoModel.funcionario), joinedload(PedidoModel.item_pedido))
            result = await session.execute(query)
            return result.unique().scalars().all()
    
    async def get_one_crud(self, id_obj: int) -> Optional[PedidoModel]:
        async with get_session() as session:
            query = select(PedidoModel).options(joinedload(PedidoModel.cliente), joinedload(PedidoModel.funcionario), joinedload(PedidoModel.item_pedido).joinedload(ItemPedidoModel.produto)).filter(PedidoModel.id == id_obj)
            result = await session.execute(query)
            return result.unique().scalars().first()

    async def get_clientes(self) -> Optional[List[ClienteModel]]:
        async with get_session() as session:
            query = select(ClienteModel)
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

    async def get_itens_pedido(self) -> Optional[List[ItemPedidoModel]]:
        async with get_session() as session:
            query = select(ItemPedidoModel)
            result = await session.execute(query)
            return result.scalars().all()

    #Criar Pedido
    async def post_crud(self) -> None:
        #Vai receber dados do formulario
        form = await self.request.form()

        cliente_id: int = int(form.get('cliente_id'))
        funcionario_id: int = int(form.get('funcionario_id'))
        data_pedido_str: str = form.get('data_pedido')
        
        # Listas dinamicas do Formulario
        produto_ids = form.getlist('produto_id')
        quantidades = form.getlist('quantidade')
        precos_unitarios = form.getlist('valor_unitario')

        #Validação básica para adicionar cliente, funcionario e data
        if not cliente_id or not funcionario_id or not data_pedido_str:
             raise ValueError("Campos obrigatórios: Cliente, Funcionário e Data.")
        
        #Validação básica para adicionar produto quantidade
        if not produto_ids or not quantidades:
             raise ValueError("Adicione pelo menos um produto ao pedido.")

        async with get_session() as session:
            pedido: PedidoModel = PedidoModel(
                cliente_id=cliente_id, 
                funcionario_id=funcionario_id, 
                data_pedido=datetime.strptime(data_pedido_str, '%Y-%m-%d') if data_pedido_str else datetime.now(),
                valor_total=0.0
            )
            session.add(pedido)
            await session.flush()

            valor_total_acumulado = 0.0

            #Iterando itens das listas
            for p_id, qtd, preco in zip(produto_ids, quantidades, precos_unitarios):
                p_id = int(p_id)
                qtd = int(qtd)
                preco = float(preco.replace(',', '.')) if isinstance(preco, str) else float(preco)

                #Cria item
                item = ItemPedidoModel(
                    pedido_id=pedido.id,
                    produto_id=p_id,
                    quantidade=qtd,
                    preco_unitario=preco
                )
                session.add(item)

                #Atualiza estoque (Saída)
                produto = await session.get(ProdutoModel, p_id)
                if produto:
                    produto.estoque -= qtd
                    session.add(produto)
                
                valor_total_acumulado += (qtd * preco)

            #Atualiza valor total de pedido
            pedido.valor_total = valor_total_acumulado
            session.add(pedido)

            await session.commit()

    #Editar um pedido
    async def put_crud(self, obj: object) -> None:
        async with get_session() as session:
            #Consultando se o pedido existe no banco
            pedido: PedidoModel = await session.get(PedidoModel, obj.id)

            if pedido:
                #Recebe os dados do form
                form = await self.request.form()

                cliente_id: int = int(form.get('cliente_id'))
                funcionario_id: int = int(form.get('funcionario_id'))
                data_pedido: str = form.get('data_pedido')
                
                if cliente_id and cliente_id != pedido.cliente_id:
                    pedido.cliente_id = int(cliente_id)

                if funcionario_id and funcionario_id != pedido.funcionario_id:
                    pedido.funcionario_id = int(funcionario_id)

                if data_pedido:
                     # Converter string para date se necessário, ou atribuir direto se o model esperar date e o driver converter
                     data_obj = datetime.strptime(data_pedido, '%Y-%m-%d')
                     if data_obj != pedido.data_pedido:
                        pedido.data_pedido = data_obj

                await session.commit()
    
    async def delete_crud(self, id_obj: int) -> None:
        async with get_session() as session:
            #Faz o Select do pedido e dos itens:
            query = select(PedidoModel).options(joinedload(PedidoModel.item_pedido)).filter(PedidoModel.id == id_obj)
            result = await session.execute(query)
            pedido = result.unique().scalars().first()

            if pedido:
                #Reverte o estoque
                for item in pedido.item_pedido:
                     # Busca o produto para garantir que ele esteja na sessão atual
                     produto = await session.get(ProdutoModel, item.produto_id)
                     if produto:
                         produto.estoque += item.quantidade
                         session.add(produto)
                
                #Deleta os itens
                for item in pedido.item_pedido:
                    await session.delete(item)
                
                #Deleta o pedido
                await session.delete(pedido)
                await session.commit()
