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
from controllers.venda_controller import VendaController
from views.admin.base_crud_view import BaseCRUDView

class VendaAdmin(BaseCRUDView):
    def __init__(self) -> None:
        self.router = APIRouter()

        self.router.routes.append(Route(path='/venda/list', endpoint=self.object_list, methods=["GET"], name="venda_list"))
        self.router.routes.append(Route(path='/venda/create', endpoint=self.object_create, methods=["GET", "POST"], name="venda_create"))
        self.router.routes.append(Route(path='/venda/details/{venda_id:int}', endpoint=self.object_edit, methods=["GET"], name="venda_details"))
        self.router.routes.append(Route(path='/venda/edit/{venda_id:int}', endpoint=self.object_edit, methods=["GET", "POST"], name="venda_edit"))
        self.router.routes.append(Route(path='/venda/delete/{venda_id:int}', endpoint=self.object_delete, methods=["GET", "DELETE"], name="venda_delete"))

        super().__init__('venda')

    #Implementação do método list
    async def object_list(self, request: Request) -> Response:
        """ Rota para listar as vendas """
        #Instancia o controller
        controller = VendaController(request)

        #Passa o controller para o método da superclasse
        return await super().object_list(object_controller=controller)

    #Implementação do método delete
    async def object_delete(self, request: Request) -> Response:
        """ Rota para deletar uma venda """
        venda_controller: VendaController = VendaController(request)

        venda_id: int = request.path_params['venda_id']
        return await super().object_delete(object_controller=venda_controller, obj_id=venda_id)
 
    #Implementação do método create
    async def object_create(self, request: Request) -> Response:
        """ Rota para criar uma venda """
        venda_controller: VendaController = VendaController(request)

        #Se o request for GET
        if request.method == "GET":
            #Adicionar o request no contexto e as listas necessárias
            fornecedores = await venda_controller.get_fornecedores()
            funcionarios = await venda_controller.get_funcionarios()
            produtos = await venda_controller.get_produtos()
            
            context = {
                'request': venda_controller.request, 
                "ano": datetime.now().year, 
                "fornecedores": fornecedores, 
                "funcionarios": funcionarios,
                "produtos": produtos
            }

            return settings.TEMPLATES.TemplateResponse(f"admin/venda/create.html", context=context)
        
        #Se o request for POST
        #Recebe os dados do formulário e cria a venda

        try:
            await venda_controller.post_crud()
        except ValueError as err:
            # Em caso de erro, re-renderizar para o usuário não perder tudo (Melhoria futura: manter dados já preenchidos)
            # Por enquanto, apenas recarregar as listas e mostrar erro
            fornecedores = await venda_controller.get_fornecedores()
            funcionarios = await venda_controller.get_funcionarios()
            produtos = await venda_controller.get_produtos()
            
            context = {
                'request': request, 
                "ano": datetime.now().year, 
                "error": err, 
                "fornecedores": fornecedores, 
                "funcionarios": funcionarios,
                "produtos": produtos
            }
            return settings.TEMPLATES.TemplateResponse(f"admin/venda/create.html", context=context)
        
        return RedirectResponse(request.url_for('venda_list'), status_code=status.HTTP_302_FOUND)

    #Implementação do método edit
    async def object_edit(self, request: Request) -> Response:
        """ Rota para editar uma venda """
        venda_controller: VendaController = VendaController(request)
        venda_id: int = request.path_params['venda_id']

        #Se o request for GET
        if request.method == "GET":
            if 'details' in str(request.url):
                return await super().object_details(object_controller=venda_controller, obj_id=venda_id)

            venda = await venda_controller.get_one_crud(id_obj=venda_id)
            
            if not venda:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            
            # Dados para o formulário
            fornecedores = await venda_controller.get_fornecedores()
            funcionarios = await venda_controller.get_funcionarios()

            context = {
                'request': request,
                'ano': datetime.now().year,
                'object': venda,
                'categorias': { 'fornecedores': fornecedores, 'funcionarios': funcionarios } 
            }

            context = {
                'request': request,
                'ano': datetime.now().year,
                'object': venda,
                'fornecedores': fornecedores,
                'funcionarios': funcionarios
            }

            return settings.TEMPLATES.TemplateResponse("admin/venda/edit.html", context=context)
        
        #Se o request for POST
        venda = await venda_controller.get_one_crud(id_obj=venda_id)

        if not venda:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        #Recebe os dados do formulário e edita a venda
        form = await request.form()
        dados: set = None

        try:
            await venda_controller.put_crud(obj=venda)
        except ValueError as err:
            nome: str = form.get('nome')
            categorias: List[str] = form.getlist('categoria')
            dados = { "nome": nome, "categorias": categorias}
            context = {'request': request, "ano": datetime.now().year, 'error': err, 'objeto': dados}
            return settings.TEMPLATES.TemplateResponse(f"admin/venda/edit.html", context=context)
        
        return RedirectResponse(request.url_for("venda_list"), status_code=status.HTTP_302_FOUND)

venda_admin = VendaAdmin()
