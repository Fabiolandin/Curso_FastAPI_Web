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
from controllers.produto_controller import ProdutoController
from views.admin.base_crud_view import BaseCRUDView

class ProdutoAdmin(BaseCRUDView):

    def __init__(self) -> None:
        self.router = APIRouter()

        self.router.routes.append(Route(path='/produto/list', endpoint=self.object_list, methods=["GET"], name="produto_list"))
        self.router.routes.append(Route(path='/produto/create', endpoint=self.object_create, methods=["GET", "POST"], name="produto_create"))
        self.router.routes.append(Route(path='/produto/details/{produto_id:int}', endpoint=self.object_edit, methods=["GET"], name="produto_details"))
        self.router.routes.append(Route(path='/produto/edit/{produto_id:int}', endpoint=self.object_edit, methods=["GET", "POST"], name="produto_edit"))
        self.router.routes.append(Route(path='/produto/delete/{produto_id:int}', endpoint=self.object_delete, methods=["GET", "DELETE"], name="produto_delete"))

        super().__init__('produto')

    #Implementa o método list
    async def object_list(self, request: Request) -> Response:
        """ Rota para listar os produtos """
        #Instancia o controller
        produto_controller = ProdutoController(request)

        #Passa o controller para o método da superclasse
        return await super().object_list(object_controller=produto_controller)

    #Implementa o método delete
    async def object_delete(self, request: Request) -> Response:
        """ Rota para deletar um produto """
        produto_controller: ProdutoController = ProdutoController(request)

        produto_id: int = request.path_params['produto_id']
        return await super().object_delete(object_controller=produto_controller, obj_id=produto_id)

    #Implementa o método create
    async def object_create(self, request: Request) -> Response:
        """ Rota para criar um produto """
        produto_controller: ProdutoController = ProdutoController(request)

        #Se o request for GET
        if request.method == "GET":
            #Adicionar o request no contexto e as categorias
            categorias = await produto_controller.get_categorias()
            context = {'request': produto_controller.request, "ano": datetime.now().year, "categorias": categorias}

            return settings.TEMPLATES.TemplateResponse(f"admin/produto/create.html", context=context)
        
        #Se o request for POST
        #Recebe os dados do formulário e cria o produto
        form = await request.form()
        dados: set = None

        try:
            await produto_controller.post_crud()
        except ValueError as err:
            nome: str = form.get('nome')
            categorias: List[str] = form.getlist('categoria')
            dados: set = { "nome": nome, "categorias": categorias}
            context = {'request': request, "ano": datetime.now().year, "erro": err, "objeto": dados}
            return settings.TEMPLATES.TemplateResponse(f"admin/produto/create.html", context=context)
        
        return RedirectResponse(request.url_for('produto_list'), status_code=status.HTTP_302_FOUND)

    #Implementa o método edit
    async def object_edit(self, request: Request) -> Response:
        """ Rota para editar um produto """

        produto_controller: ProdutoController = ProdutoController(request)
        produto_id: int = request.path_params['produto_id']

        #Se o request for GET
        if request.method == "GET":
            produto = await produto_controller.get_one_crud(id_obj=produto_id)
            
            if not produto:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            
            # Todas as categorias disponíveis
            categorias = await produto_controller.get_categorias()

            # IDs das categorias que o produto já possui
            categorias_list = [categoria.id for categoria in produto.categorias] if produto.categorias else []

            context = {
                'request': request,
                'ano': datetime.now().year,
                'object': produto,
                'categorias': categorias,
                'categorias_list': categorias_list
            }

            return settings.TEMPLATES.TemplateResponse("admin/produto/edit.html", context=context)
        
        #Se o request for POST
        produto = await produto_controller.get_one_crud(id_obj=produto_id)

        if not produto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        #Recebe os dados do formulário e edita o produto
        form = await request.form()
        dados: set = None

        try:
            await produto_controller.put_crud(obj=produto)
        except ValueError as err:
            nome: str = form.get('nome')
            categorias: List[str] = form.getlist('categoria')
            dados = { "nome": nome, "categorias": categorias}
            context = {'request': request, "ano": datetime.now().year, 'error': err, 'objeto': dados}
            return settings.TEMPLATES.TemplateResponse(f"admin/produto/edit.html", context=context)
        
        return RedirectResponse(request.url_for("produto_list"), status_code=status.HTTP_302_FOUND)

produto_admin = ProdutoAdmin()
        