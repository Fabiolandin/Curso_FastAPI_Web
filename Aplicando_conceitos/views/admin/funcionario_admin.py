from datetime import datetime

from fastapi.routing import APIRouter
#Montar as rotas manualmente
from starlette.routing import Route

from fastapi import status
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse
from fastapi.exceptions import HTTPException

from core.configs import settings
from controllers.funcionario_controller import FuncionarioController
from views.admin.base_crud_view import BaseCRUDView


class FuncionarioAdmin(BaseCRUDView):

    def __init__(self) -> None:
        self.router = APIRouter()

        self.router.routes.append(Route(path="/funcionario/list", endpoint=self.object_list, methods=["GET"], name="funcionario_list"))
        self.router.routes.append(Route(path="/funcionario/create", endpoint=self.object_create, methods=["GET", "POST"], name="funcionario_create"))
        self.router.routes.append(Route(path="/funcionario/details/{funcionario_id:int}", endpoint=self.object_edit, methods=["GET"], name="funcionario_details"))
        self.router.routes.append(Route(path="/funcionario/edit/{funcionario_id:int}", endpoint=self.object_edit, methods=["GET", "POST"], name="funcionario_edit"))
        self.router.routes.append(Route(path="/funcionario/delete/{funcionario_id:int}", endpoint=self.object_delete, methods=["GET", "DELETE"], name="funcionario_delete"))

        super().__init__("funcionario")

    #Implementa o método de listagem
    async def object_list(self, request: Request) -> Response:
        """ Rota para listar os funcionários """
        #Instancia o controller com o request
        funcionario_controller = FuncionarioController(request)

        #Passa o controler para o método genérico da superclasse
        return await super().object_list(object_controller=funcionario_controller)

    #Método delete
    async def object_delete(self, request: Request) -> Response:
        """ Rota para deletar um funcionário """
        funcionario_controller: FuncionarioController = FuncionarioController(request)

        funcionario_id: int = request.path_params['funcionario_id']
        return await super().object_delete(object_controller=funcionario_controller, obj_id=funcionario_id)

    async def object_create(self, request: Request) -> Response:
        """ Rota para criar um funcionário """
        funcionario_controller: FuncionarioController = FuncionarioController(request)

        #Se o request for GET
        if request.method == "GET":
            context = {"request": request, "ano": datetime.now().year}

            return settings.TEMPLATES.TemplateResponse(f"admin/funcionario/create.html", context=context)
        
        #Se o request for POST
        form = await request.form()
        dados: set = None

        try:
            await funcionario_controller.post_crud()
        except ValueError as err:
            nome: str = form.get("nome")
            cpf_cnpj: str = form.get("cpf_cnpj")
            telefone: str = form.get("telefone")
            email: str = form.get("email")
            dados = {"nome": nome, "cpf_cnpj": cpf_cnpj, "telefone": telefone, "email": email}
            context = {'request': request, "ano": datetime.now().year, "error": err, 'objeto': dados}
            return settings.TEMPLATES.TemplateResponse(f"admin/funcionario/create.html", context=context)
        
        return RedirectResponse(request.url_for("funcionario_list"), status_code=status.HTTP_302_FOUND)

    async def object_edit(self, request: Request) -> Response:
        """ Rota para editar um funcionário """
        funcionario_controller = FuncionarioController(request)
        funcionario_id: int = request.path_params['funcionario_id']

        if request.method == "GET":
            return await super().object_details(object_controller=funcionario_controller, obj_id=funcionario_id)
        
        #Se o request for POST
        funcionario = await funcionario_controller.get_one_crud(funcionario_id)

        if not funcionario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Funcionário não encontrado")

        #Pega os dados do form
        form = await request.form()
        dados: set = None

        try: await funcionario_controller.put_crud(obj=funcionario)
        except ValueError as err:
            nome: str = form.get("nome")
            cpf: str = form.get("cpf")
            cargo: str = form.get("cargo")
            data_admissao: str = form.get("data_admissao")
            dados = {"nome": nome, "cpf": cpf, "cargo": cargo, "data_admissao": data_admissao}
            context = {'request': request, "ano": datetime.now().year, "error": err, 'objeto': dados}
            return settings.TEMPLATES.TemplateResponse(f"admin/funcionario/edit.html", context=context)
        
        return RedirectResponse(request.url_for("funcionario_list"), status_code=status.HTTP_302_FOUND)

funcionario_admin = FuncionarioAdmin()