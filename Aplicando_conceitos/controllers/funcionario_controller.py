from fastapi.requests import Request

from datetime import datetime
from core.configs import settings
from core.database import get_session
from models.funcionario_model import FuncionarioModel
from controllers.base_controller import BaseController

class FuncionarioController(BaseController):

    def __init__(self, request: Request) -> None:
        super().__init__(request, FuncionarioModel)

    #Criar um funcionario
    async def post_crud(self) -> None:
        #Recebe os dados do formulario
        form = await self.request.form()
        
        nome: str = form.get('nome')
        cpf: str = form.get('cpf')
        cargo: str = form.get('cargo')
        data_admissao: str = form.get('data_admissao')

        #Validação para que os campos nome, cpf, cargo e data_admissao sejam obrigatórios!
        if not nome or not cpf or not cargo or not data_admissao:
            raise ValueError("Todos os campos são obrigatórios.")
        
        #Instanciar o objeto
        funcionario: FuncionarioModel = FuncionarioModel(nome=nome, cpf=cpf, cargo=cargo, data_admissao=data_admissao)

        #Cria a sessão e insere no banco
        async with get_session() as session:
            session.add(funcionario)
            await session.commit()

    
    #Editar um funcionario
    async def put_crud(self, obj: object) -> None:
        async with get_session() as session:
            #Consultando se o funcionario existe no banco
            funcionario: FuncionarioModel = await session.get(self.model, obj.id)

            if funcionario:
                #Recebe os dados do formulario
                form = await self.request.form()

                nome: str = form.get('nome')
                cpf: str = form.get('cpf')
                cargo: str = form.get('cargo')
                data_admissao: str = form.get('data_admissao')

                #O nome que recebemos é diferente do que está no banco?
                if nome and nome != funcionario.nome:
                    funcionario.nome = nome

                #O cpf que recebemos é diferente do que está no banco?
                if cpf and cpf != funcionario.cpf:
                    funcionario.cpf = cpf

                #O cargo que recebemos é diferente do que está no banco?
                if cargo and cargo != funcionario.cargo:
                    funcionario.cargo = cargo

                #A data_admissao que recebemos é diferente do que está no banco?
                if data_admissao and data_admissao != funcionario.data_admissao:
                    funcionario.data_admissao = data_admissao

                session.add(funcionario)
                await session.commit()