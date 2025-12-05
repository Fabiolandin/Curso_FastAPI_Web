from datetime import datetime

from fastapi.routing import APIRouter
#Montar as rotas manualmente
from starlette.routing import Route

from fastapi import status
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse
from fastapi.exceptions import HTTPException

from core.configs import settings
from controllers.categoria_produto_controller import CategoriaProdutoController
from views.admin.base_crud_view import BaseCRUDView


class CategoriaProdutoAdmin(BaseCRUDView):

    def __init__(self) -> None:
        self.router = APIRouter()

        self.router.routes.append(Route(path="/categoria_produto/list", endpoint=self.object_list, methods=["GET"], name="categoria_produto_list"))
        self.router.routes.append(Route(path="/categoria_produto/create", endpoint=self.object_create, methods=["GET", "POST"], name="categoria_produto_create"))
        self.router.routes.append(Route(path="/categoria_produto/details/{categoria_produto_id:int}", endpoint=self.object_edit, methods=["GET"], name="categoria_produto_details"))
        self.router.routes.append(Route(path="/categoria_produto/edit/{categoria_produto_id:int}", endpoint=self.object_edit, methods=["GET", "POST"], name="categoria_produto_edit"))
        self.router.routes.append(Route(path="/categoria_produto/delete/{categoria_produto_id:int}", endpoint=self.object_delete, methods=["GET", "DELETE"], name="categoria_produto_delete"))

        super().__init__("categoria_produto")
    
    #Implementação do método de listagem
    async def object_list(self, request: Request) -> Response:
        """ Rota para listar as categorias de produtos """
        #Instancia o controller com o request
        categoria_produto_controller = CategoriaProdutoController(request)

        #Passa o controler para o método genérico da superclasse
        return await super().object_list(object_controller=categoria_produto_controller)

    #Método delete
    async def object_delete(self, request: Request) -> Response:
        """ Rota para deletar uma categoria de produto """
        categoria_produto_controller: CategoriaProdutoController = CategoriaProdutoController(request)

        categoria_produto_id: int = request.path_params['categoria_produto_id']
        return await super().object_delete(object_controller=categoria_produto_controller, obj_id=categoria_produto_id)

    #Método create
    async def object_create(self, request: Request) -> Response:
        """ Rota para criar uma categoria """
        categoria_produto_controller: CategoriaProdutoController = CategoriaProdutoController(request)

        #Se o request for GET
        if request.method == "GET":
            context = {"request": request, "ano": datetime.now().year}

            return settings.TEMPLATES.TemplateResponse(f"admin/categoria_produto/create.html", context=context)

        #Se o request for POST
        form = await request.form()
        dados: set = None

        try:
            await categoria_produto_controller.post_crud()
        except ValueError as err:
            nome: str = form.get("nome")
            descricao: str = form.get("descricao")
            dados = {"nome": nome, "descricao": descricao}
            context = {'request': request, "ano": datetime.now().year, "error": err, 'objeto': dados}
            return settings.TEMPLATES.TemplateResponse(f"admin/categoria_produto/create.html", context=context)
        
        return RedirectResponse(request.url_for("categoria_produto_list"), status_code=status.HTTP_302_FOUND)

    #Método edit
    async def object_edit(self, request: Request) -> Response:
        """ Rota para editar uma categoria """
        categoria_produto_controller: CategoriaProdutoController = CategoriaProdutoController(request)
        categoria_produto_id: int = request.path_params['categoria_produto_id']

        #Se o request for GET
        if request.method == "GET":
            return await super().object_details(object_controller=categoria_produto_controller, obj_id=categoria_produto_id)

        #Se o request for POST
        categoria_produto = await categoria_produto_controller.get_one_crud(id_obj=categoria_produto_id)

        if not categoria_produto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        #Pega os dados do form
        form = await request.form()
        dados: set = None

        try:
            await categoria_produto_controller.put_crud(obj=categoria_produto)
        except ValueError as err:
            nome: str = form.get("nome")
            descricao: str = form.get("descricao")
            dados = {"nome": nome, "descricao": descricao}
            context = {'request': request, "ano": datetime.now().year, "error": err, 'objeto': dados}
            return settings.TEMPLATES.TemplateResponse(f"admin/categoria_produto/edit.html", context=context)
        
        return RedirectResponse(request.url_for("categoria_produto_list"), status_code=status.HTTP_302_FOUND)