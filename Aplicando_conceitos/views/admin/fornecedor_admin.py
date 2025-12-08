from datetime import datetime

from fastapi.routing import APIRouter
#Montar as rotas manualmente
from starlette.routing import Route

from fastapi import status
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse
from fastapi.exceptions import HTTPException

from core.configs import settings
from controllers.fornecedor_controller import FornecedorController
from views.admin.base_crud_view import BaseCrudView


class FornecedorAdmin(BaseCrudView):

    def __init__(self) -> None:
        self.router = APIRouter()

        self.router.routes.append(Route(path="/fornecedor/list", endpoint=self.object_list, methods=["GET"], name="fornecedor_list"))
        self.router.routes.append(Route(path="/fornecedor/create", endpoint=self.object_create, methods=["GET", "POST"], name="fornecedor_create"))
        self.router.routes.append(Route(path="/fornecedor/details/{fornecedor_id:int}", endpoint=self.object_edit, methods=["GET"], name="fornecedor_details"))
        self.router.routes.append(Route(path="/fornecedor/edit/{fornecedor_id:int}", endpoint=self.object_edit, methods=["GET", "POST"], name="fornecedor_edit"))
        self.router.routes.append(Route(path="/fornecedor/delete/{fornecedor_id:int}", endpoint=self.object_delete, methods=["GET", "DELETE"], name="fornecedor_delete"))

        super().__init__("fornecedor")

    #Implemente o método de listagem
    async def objec_list(self, request: Request) -> Response:
        """ Rota para listar os fornecedores """
        #Instancia o controller com o request
        fornecedor_controller = FornecedorController(request)

        #Passa o controler para o método genérico da superclasse
        return await super().object_list(object_controller=fornecedor_controller)

    #Método delete
    async def object_delete(self, request: Request) -> Response:
        """ Rota para deletar um fornecedor """
        fornecedor_controller: FornecedorController = FornecedorController(request)

        fornecedor_id: int = request.path_params['fornecedor_id']
        return await super().object_delete(object_controller=fornecedor_controller, obj_id=fornecedor_id)

    async def object_create(self, request: Request) -> Response:
        """ Rota para criar um fornecedor """
        fornecedor_controller: FornecedorController = FornecedorController(request)

        #Se o request for GET
        if request.method == "GET":
            context = {"request": request, "ano": datetime.now().year}

            return settings.TEMPLATES.TemplateResponse(f"admin/fornecedor/create.html", context=context)
        
        #Se o request for POST
        form = await request.form()
        dados: set = None

        try:
            await fornecedor_controller.post_crud()
        except ValueError as err:
            nome: str = form.get("nome")
            cnpj: str = form.get("cnpj")
            dados = {"nome": nome, "cnpj": cnpj}
            context = {'request': request, "ano": datetime.now().year, "error": err, 'objeto': dados}
            return settings.TEMPLATES.TemplateResponse(f"admin/fornecedor/create.html", context=context)
        
        return RedirectResponse(request.url_for("fornecedor_list"), status_code=status.HTTP_302_FOUND)

    #Método edit
    async def object_edit(self, request: Request) -> Response:
        """ Rota para editar um fornecedor """
        fornecedor_controller = FornecedorController(request)
        fornecedor_id: int = request.path_params['fornecedor_id']

        if request.method == "GET":
            return await super().object_details(object_controller=fornecedor_controller, obj_id=fornecedor_id)
        
        #Se o request for POST
        fornecedor = await fornecedor_controller.get_one_crud(fornecedor_id)

        if not fornecedor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fornecedor não encontrado")

        #Pega os dados do form
        form = await request.form()
        dados: set = None

        try: await fornecedor_controller.put_crud(obj=fornecedor)
        except ValueError as err:
            nome: str = form.get("nome")
            cnpj: str = form.get("cnpj")
            dados = {"nome": nome, "cnpj": cnpj}
            context = {'request': request, "ano": datetime.now().year, "error": err, 'objeto': dados}
            return settings.TEMPLATES.TemplateResponse(f"admin/fornecedor/edit.html", context=context)
        
        return RedirectResponse(request.url_for("fornecedor_list"), status_code=status.HTTP_302_FOUND)

fornecedor_admin = FornecedorAdmin()