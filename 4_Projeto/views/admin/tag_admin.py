from datetime import datetime

from fastapi.routing import APIRouter
#Montar as rotas manualmente
from starlette.routing import Route

from fastapi import status
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse
from fastapi.exceptions import HTTPException

from core.configs import settings
from controllers.tag_controller import TagController
from views.admin.base_crud_view import BaseCRUDView


class TagAdmin(BaseCRUDView):

    def __init__(self) -> None:
        self.router = APIRouter()

        self.router.routes.append(Route(path='/tag/list', endpoint=self.object_list, methods=["GET"], name="tag_list"))
        self.router.routes.append(Route(path='/tag/create', endpoint=self.object_create, methods=["GET", "POST"], name="tag_create"))
        self.router.routes.append(Route(path='/tag/details/{tag_id:int}', endpoint=self.object_edit, methods=["GET"], name="tag_details"))
        self.router.routes.append(Route(path='/tag/edit/{tag_id:int}', endpoint=self.object_edit, methods=["GET", "POST"], name="tag_edit"))
        self.router.routes.append(Route(path='/tag/delete/{tag_id:int}', endpoint=self.object_delete, methods=["GET", "DELETE"], name="tag_delete"))

        super().__init__('tag')

    #Implementa o método
    async def object_list(self, request: Request) -> Response:
        """ Rota para listar as tags """
        #Instancia o controller
        tag_controller = TagController(request)

        #Passa o controller para o método da superclasse
        return await super().object_list(object_controller=tag_controller)
    
    #Implementa o método
    async def object_delete(self, request: Request) -> Response:
        """ Rota para deletar uma tag """
        tag_controller: TagController = TagController(request)

        tag_id: int = request.path_params['tag_id']
        return await super().object_delete(object_controller=tag_controller, obj_id=tag_id)
    
    #Implementa o método
    async def object_create(self, request: Request) -> Response:
        """ Rota para criar uma tag """
        tag_controller: TagController = TagController(request)

        #Se o request for GET
        if request.method == 'GET':
            #Adicionar o request no contexto
            context = {'request': tag_controller.request, "ano": datetime.now().year}

            return settings.TEMPLATES.TemplateResponse(f"admin/tag/create.html", context=context)
        
        #Se o request for POST
        #Recebe os dados do formulário e cria a tag
        try:
            await tag_controller.post_crud()
            #Redireciona para a lista de tags
        except ValueError as err:
            tag: str = (await request.form()).get('tag')
            dados: set = { "tag": tag }
            context = {'request': request, "ano": datetime.now().year, "erro": err, "objeto": dados}
            return settings.TEMPLATES.TemplateResponse(f"admin/tag/create.html", context=context)
        
        return RedirectResponse(request.url_for('tag_list'), status_code=status.HTTP_302_FOUND)
    
    #Implementa o método
    async def object_edit(self, request: Request) -> Response:
        """ Rota para carregar o template de edição da tag """

        tag_controller: TagController = TagController(request)
        tag_id: int = request.path_params['tag_id']

        #Se o request for GET
        if request.method == 'GET':
            return await super().object_details(object_controller=tag_controller, obj_id=tag_id)
        
        #Se o request for POST
        tag = await tag_controller.get_one_crud(id_obj=tag_id)

        if not tag:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        #Recebe os dados do formulário e edita a tag
        form = await request.form()
        dados: set = None

        try:
            await tag_controller.put_crud(obj=tag)
        except ValueError as err:
            tag: str = form.get('tag')
            dados = {"tag": tag}
            context = {'request': request, "ano": datetime.now().year, "erro": err, "objeto": dados}
            return settings.TEMPLATES.TemplateResponse(f"admin/tag/edit.html", context=context)

        return RedirectResponse(request.url_for('tag_list'), status_code=status.HTTP_302_FOUND)
    
tag_admin = TagAdmin()