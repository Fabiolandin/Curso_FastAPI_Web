from fastapi.requests import Request
from typing import List, Optional

from sqlalchemy.future import select

from core.configs import settings
from core.database import get_session
from models.compra_model import CompraModel
from models.fornecedor_model import FornecedorModel
from models.funcionario_model import FuncionarioModel
from models.item_compra_model import ItemCompraModel
from controllers.base_controller import BaseController
from sqlalchemy.orm import joinedload

class CompraController(BaseController):

    def __init__(self, request: Request) -> None:
        super().__init__(request, CompraModel)

    async def get_all_crud(self) -> Optional[List[CompraModel]]:
        async with get_session() as session:
            query = select(CompraModel).options(joinedload(CompraModel.fornecedor), joinedload(CompraModel.funcionario), joinedload(CompraModel.item_compra))
            result = await session.execute(query)
            return result.scalars().all()

    async def get_one_crud(self, id_obj: int) -> Optional[CompraModel]:
        async with get_session() as session:
            query = select(CompraModel).options(joinedload(CompraModel.fornecedor), joinedload(CompraModel.funcionario), joinedload(CompraModel.item_compra)).filter(CompraModel.id == id_obj)
            result = await session.execute(query)
            return result.scalars().first()

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

    async def get_itens_compra(self) -> Optional[List[ItemCompraModel]]:
        async with get_session() as session:
            query = select(ItemCompraModel)
            result = await session.execute(query)
            return result.scalars().all()

    #Criar uma compra
    async def post_crud(self) -> None:
    
        #Vai receber dados do formulario.ArithmeticError
        form = await self.request.form()

        fornecedor_id: int = form.get('fornecedor_id')
        funcionario_id: int = form.get('funcionario_id')
        data_compra: datetime = form.get('data_compra')
        valor_total: float = 0.0

        #Validação para que todos os campos sejam obrigatórios!
        if not fornecedor_id or not funcionario_id or not data_compra or not valor_total:
            raise ValueError("Todos os campos são obrigatórios.")

        #Instanciar o objeto
        compra: CompraModel = CompraModel(fornecedor_id=int(fornecedor_id), funcionario_id=int(funcionario_id), data_compra=data_compra)

        async with get_session() as session:
            session.add(compra)
            await session.commit()

    #Editar um produto
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