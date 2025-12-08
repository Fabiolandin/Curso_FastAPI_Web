from fastapi.requests import Request

from datetime import datetime
from core.configs import settings
from core.database import get_session
from models.fornecedor_model import FornecedorModel
from controllers.base_controller import BaseController

class FornecedorController(BaseController):
    def __init__(self, request: Request) -> None:
        super().__init__(request, FornecedorModel)

    #Criar um fornecedor
    async def post_crud(self) -> None:
        #Recebe os dados do formulario
        form = await self.request.form()
        
        nome: str = form.get('nome')
        cnpj: str = form.get('cnpj')
        telefone: str = form.get('telefone')
        email: str = form.get('email')

        #Validação para que os campos nome, cnpj, telefone e email sejam obrigatórios!
        if not nome or not cnpj or not telefone or not email:
            raise ValueError("Todos os campos são obrigatórios.")

        #Instanciar o objeto
        fornecedor: FornecedorModel = FornecedorModel(nome=nome, cnpj=cnpj, telefone=telefone, email=email)

        #Cria a sessão e insere no banco
        async with get_session() as session:
            session.add(fornecedor)
            await session.commit()

    #Editar um fornecedor
    async def put_crud(self, obj: object) -> None:
        async with get_session() as session:
            #Consultando se o fornecedor existe no banco
            fornecedor: FornecedorModel = await session.get(self.model, obj.id)

            if fornecedor:
                #Recebe os dados do formulario
                form = await self.request.form()

                nome: str = form.get('nome')
                cnpj: str = form.get('cnpj')
                telefone: str = form.get('telefone')
                email: str = form.get('email')

                #O nome que recebemos é diferente do que está no banco?
                if nome and nome != fornecedor.nome:
                    fornecedor.nome = nome

                #O cnpj que recebemos é diferente do que está no banco?
                if cnpj and cnpj != fornecedor.cnpj:
                    fornecedor.cnpj = cnpj

                #O telefone que recebemos é diferente do que está no banco?
                if telefone and telefone != fornecedor.telefone:
                    fornecedor.telefone = telefone

                #O email que recebemos é diferente do que está no banco?
                if email and email != fornecedor.email:
                    fornecedor.email = email

                session.add(fornecedor)
                await session.commit()
        
        
