from fastapi.requests import Request

from datetime import datetime
from core.configs import settings
from core.database import get_session
from models.cliente_model import ClienteModel
from controllers.base_controller import BaseController


class ClienteController(BaseController):

    def __init__(self, request: Request) -> None:
        super().__init__(request, ClienteModel)

    #Criar um cliente
    async def post_crud(self) -> None:
        #Recebe dados do formulario
        form = await self.request.form()

        nome: str = form.get('nome')
        cpf_cnpj: str = form.get('cpfcnpj')
        telefone: str = form.get('telefone')
        email: str = form.get('email')
        data_de_cadastro: datetime = datetime.now()

        #Validação para que os campos nome email e telefone sejam obrigatórios!
        if not nome or not email or not telefone:
            raise ValueError("Todos os campos são obrigatórios.")
        
        #Instanciar o objeto
        cliente: ClienteModel = ClienteModel(nome=nome, cpf_cnpj=cpf_cnpj, telefone=telefone, email=email, data_de_cadastro=data_de_cadastro)

        #Cria a sessão e insere no banco
        async with get_session() as session:
            session.add(cliente)
            await session.commit()

    
    #Edit de cliente
    async def put_crud(self, obj: object) -> None:
        async with get_session() as session:
            #Consultando se o cliente existe no banco
            cliente: ClienteModel = await session.get(self.model, obj.id)

            if cliente:
                #Recebe os dados do formulario
                form = await self.request.form()

                nome: str = form.get('nome')
                cpf_cnpj: str = form.get('cpfcnpj')
                telefone: str = form.get('telefone')
                email: str = form.get('email')

                #O nome que recebemos é diferente do que está no banco?
                if nome and nome != cliente.nome:
                    cliente.nome = nome

                #O cpf_cnpj que recebemos é diferente do que está no banco?
                if cpf_cnpj and cpf_cnpj != cliente.cpf_cnpj:
                    cliente.cpf_cnpj = cpf_cnpj

                #O telefone que recebemos é diferente do que está no banco?
                if telefone and telefone != cliente.telefone:
                    cliente.telefone = telefone

                #O email que recebemos é diferente do que está no banco?
                if email and email != cliente.email:
                    cliente.email = email

                session.add(cliente)
                await session.commit()
