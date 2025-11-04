from datetime import datetime

from fastapi.routing import APIRouter
#Montar as rotas manualmente
from starlette.routing import Route

from fastapi import status
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse
from fastapi.exceptions import HTTPException

from core.configs import settings
from controllers.cliente_controller import ClienteController
from views.admin.base_crud_view import BaseCRUDView


class ClienteAdmin(BaseCRUDView):

    def __init__(self) -> None:
        self.router = APIRouter()

        self.router.routes.append(Route(path="/cliente/list", endpoint=self.object_details_list, methods=["GET"], name="cliente_list"))
        self.router.routes.append(Route(path="/cliente/create", endpoint=self.object_create, methods=["GET", "POST"], name="cliente_create"))
        self.router.routes.append(Route(path="/cliente/details/{cliente_id:int}", endpoint=self.object_details, methods=["GET"], name="cliente_details"))
        self.router.routes.append(Route(path="/cliente/edit/{cliente_id:int}", endpoint=self.object_edit, methods=["GET", "POST"], name="cliente_edit"))
        self.router.routes.append(Route(path="/cliente/delete/{cliente_id:int}", endpoint=self.object_delete, methods=["GET"], name="cliente_delete"))

        super().__init__("cliente")

    #Implementa o método de listagem
    async def object_details_list(self, request: Request) -> Response:
        """ Rota para listar os clientes """
        #Instantia o controller com o request
        cliente_controller = ClienteController(request)

        #Passa o controler para o método genérico da superclasse
        return await super().object_list(object_controller=cliente_controller)
    
    async def object_delete(self, request: Request) -> Response:
        """ Rota para deletar um cliente """
        cliente_controller: ClienteController = ClienteController(request)

        cliente_id: int = request.path_params['cliente_id']
        return await super().object_delete(object_controller=cliente_controller, obj_id=cliente_id)
    
    async def object_create(self, request: Request) -> Response:
        """ Rota para criar um cliente """
        cliente_controller: ClienteController = ClienteController(request)

        #Se o request for GET
        if request.method == "GET":
            context = {"request": request, "ano": datetime.now().year}

            return settings.TEMPLATES.TemplateResponse(f"admin/cliente/create.html", context=context)
        
        #Se o request for POST
        form = await request.form()
        dados: set = None

        try:
            await cliente_controller.post_crud()
        except ValueError as err:
            nome: str = form.get("nome")
            cpf_cnpj: str = form.get("cpf_cnpj")
            telefone: str = form.get("telefone")
            email: str = form.get("email")
            context = {'request': request, "ano": datetime.now().year, "error": err, 'objeto': dados}
            return settings.TEMPLATES.TemplateResponse(f"admin/cliente/create.html", context=context)
        
        return RedirectResponse(request.url_for("cliente_list"), status_code=status.HTTP_302_FOUND)
    
    async def object_edit(self, request: Request) -> Response:
        """ Rota para editar um cliente """
        cliente_controller: ClienteController = ClienteController(request)
        cliente_id: int = request.path_params['cliente_id']

        #Se o request for GET
        if request.method == "GET":
            return await super().object_details(object_controller=cliente_controller, obj_id=cliente_id)
        
        #Se o request for POST
        cliente = await cliente_controller.get_one_crud(id_obj=cliente_id)

        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        #Pega os dados do form
        form = await request.form()
        dados: set = None

        try:
            await cliente_controller.put_crud(obj=cliente)
        except ValueError as err:
            nome: str = form.get("nome")
            cpf_cnpj: str = form.get("cpf_cnpj")
            telefone: str = form.get("telefone")
            email: str = form.get("email")
            dados = {"nome": nome, "cpf_cnpj": cpf_cnpj, "telefone": telefone, "email": email}
            context = {'request': request, "ano": datetime.now().year, "error": err, 'objeto': dados}
            return settings.TEMPLATES.TemplateResponse(f"admin/cliente/edit.html", context=context)
        
        return RedirectResponse(request.url_for("cliente_list"), status_code=status.HTTP_302_FOUND)
    
cliente_admin = ClienteAdmin()
    





