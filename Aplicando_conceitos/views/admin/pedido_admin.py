from datetime import datetime
from typing import List

from fastapi.routing import APIRouter
#Montar as rotas manualmente
from starlette.routing import Route

from fastapi import status
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse
from fastapi.exceptions import HTTPException

from core.configs import settings
from controllers.pedido_controller import PedidoController
from views.admin.base_crud_view import BaseCRUDView

class PedidoAdmin(BaseCRUDView):
    def __init__(self) -> None:
        self.router = APIRouter()

        self.router.routes.append(Route(path='/pedido/list', endpoint=self.object_list, methods=["GET"], name="pedido_list"))
        self.router.routes.append(Route(path='/pedido/create', endpoint=self.object_create, methods=["GET", "POST"], name="pedido_create"))
        self.router.routes.append(Route(path='/pedido/details/{pedido_id:int}', endpoint=self.object_edit, methods=["GET"], name="pedido_details"))
        self.router.routes.append(Route(path='/pedido/edit/{pedido_id:int}', endpoint=self.object_edit, methods=["GET", "POST"], name="pedido_edit"))
        self.router.routes.append(Route(path='/pedido/delete/{pedido_id:int}', endpoint=self.object_delete, methods=["GET", "DELETE"], name="pedido_delete"))

        super().__init__('pedido')

    #Implementação do método list
    async def object_list(self, request: Request) -> Response:
        """ Rota para listar os pedidos """
        #Instancia o controller
        controller = PedidoController(request)

        #Passa o controller para o método da superclasse
        return await super().object_list(object_controller=controller)

    #Implementação do método delete
    async def object_delete(self, request: Request) -> Response:
        """ Rota para deletar um pedido """
        pedido_controller: PedidoController = PedidoController(request)

        pedido_id: int = request.path_params['pedido_id']
        return await super().object_delete(object_controller=pedido_controller, obj_id=pedido_id)
 
    #Implementação do método create
    async def object_create(self, request: Request) -> Response:
        """ Rota para criar um pedido """
        pedido_controller: PedidoController = PedidoController(request)

        #Se o request for GET
        if request.method == "GET":
            #Adicionar o request no contexto e as listas necessárias
            clientes = await pedido_controller.get_clientes()
            funcionarios = await pedido_controller.get_funcionarios()
            produtos = await pedido_controller.get_produtos()
            
            context = {
                'request': pedido_controller.request, 
                "ano": datetime.now().year, 
                "clientes": clientes, 
                "funcionarios": funcionarios,
                "produtos": produtos
            }

            return settings.TEMPLATES.TemplateResponse(f"admin/pedido/create.html", context=context)
        
        #Se o request for POST
        #Recebe os dados do formulário e cria a venda

        try:
            await pedido_controller.post_crud()
        except ValueError as err:
            # Em caso de erro, re-renderizar para o usuário não perder tudo (Melhoria futura: manter dados já preenchidos)
            # Por enquanto, apenas recarregar as listas e mostrar erro
            clientes = await pedido_controller.get_clientes()
            funcionarios = await pedido_controller.get_funcionarios()
            produtos = await pedido_controller.get_produtos()
            
            context = {
                'request': request, 
                "ano": datetime.now().year, 
                "error": err, 
                "clientes": clientes, 
                "funcionarios": funcionarios,
                "produtos": produtos
            }
            return settings.TEMPLATES.TemplateResponse(f"admin/pedido/create.html", context=context)
        
        return RedirectResponse(request.url_for('pedido_list'), status_code=status.HTTP_302_FOUND)

    #Implementação do método edit
    async def object_edit(self, request: Request) -> Response:
        """ Rota para editar um pedido """
        pedido_controller: PedidoController = PedidoController(request)
        pedido_id: int = request.path_params['pedido_id']

        #Se o request for GET
        if request.method == "GET":
            if 'details' in str(request.url):
                return await super().object_details(object_controller=pedido_controller, obj_id=pedido_id)

            pedido = await pedido_controller.get_one_crud(id_obj=pedido_id)
            
            if not pedido:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            
            # Dados para o formulário
            clientes = await pedido_controller.get_clientes()
            funcionarios = await pedido_controller.get_funcionarios()

            context = {
                'request': request,
                'ano': datetime.now().year,
                'object': pedido,
                'clientes': clientes,
                'funcionarios': funcionarios
            }

            return settings.TEMPLATES.TemplateResponse("admin/pedido/edit.html", context=context)
        
        #Se o request for POST
        pedido = await pedido_controller.get_one_crud(id_obj=pedido_id)

        if not pedido:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        #Recebe os dados do formulário e edita
        form = await request.form()
        dados: set = None

        try:
            await pedido_controller.put_crud(obj=pedido)
        except ValueError as err:
            context = {'request': request, "ano": datetime.now().year, 'error': err}
            return settings.TEMPLATES.TemplateResponse(f"admin/pedido/edit.html", context=context)
        
        return RedirectResponse(request.url_for("pedido_list"), status_code=status.HTTP_302_FOUND)

pedido_admin = PedidoAdmin()
