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
from controllers.autor_controller import AutorController
from views.admin.base_crud_view import BaseCRUDView



class AutorAdmin(BaseCRUDView):

    def __init__(self) -> None:
        self.router = APIRouter()

        self.router.routes.append(Route(path='/autor/list', endpoint=self.object_list, methods=["GET"], name="autor_list"))
        self.router.routes.append(Route(path='/autor/create', endpoint=self.object_create, methods=["GET", "POST"], name="autor_create"))
        self.router.routes.append(Route(path='/autor/details/{autor_id:int}', endpoint=self.object_edit, methods=["GET"], name="autor_details"))
        self.router.routes.append(Route(path='/autor/edit/{autor_id:int}', endpoint=self.object_edit, methods=["GET", "POST"], name="autor_edit"))
        self.router.routes.append(Route(path='/autor/delete/{autor_id:int}', endpoint=self.object_delete, methods=["GET", "DELETE"], name="autor_delete"))

        super().__init__('autor')

    #Implementa o método
    async def object_list(self, request: Request) -> Response:
        """ Rota para listar os autores """
        #Instancia o controller
        autor_controller = AutorController(request)

        #Passa o controller para o método da superclasse
        return await super().object_list(object_controller=autor_controller)

    #Implementa o método
    async def object_delete(self, request: Request) -> Response:
        """ Rota para deletar um autor """
        autor_controller: AutorController = AutorController(request)

        autor_id: int = request.path_params['autor_id']
        return await super().object_delete(object_controller=autor_controller, obj_id=autor_id)
    
    #Implementa o método
    async def object_create(self, request: Request) -> Response:
        """ Rota para criar um autor """
        autor_controller: AutorController = AutorController(request)

        #Se o request for GET
        if request.method == 'GET':
            #Adicionar o request no contexto, e as tags
            tags = await autor_controller.get_tags()
            context = {'request': autor_controller.request, "ano": datetime.now().year, "tags": tags}

            return settings.TEMPLATES.TemplateResponse(f"admin/autor/create.html", context=context)
        
        #Se o request for POST
        #Recebe os dados do formulário e cria o autor
        form = await request.form()
        dados: set = None

        try:
            await autor_controller.post_crud()
        except ValueError as err:
            nome: str = form.get('nome')
            tags: List(str) = form.get('tag')
            dados: set = { "nome": nome, "tags": tags}
            context = {'request': request, "ano": datetime.now().year, "erro": err, "objeto": dados}
            return settings.TEMPLATES.TemplateResponse(f"admin/autor/create.html", context=context)
        
        return RedirectResponse(request.url_for('autor_list'), status_code=status.HTTP_302_FOUND)

    #Implementa o método
    async def object_edit(self, request: Request) -> Response:
        """ Rota para carregar o template de edição do autor """

        autor_controller: AutorController = AutorController(request)
        autor_id: int = request.path_params['autor_id']

        #Se o request for GET
        if request.method == 'GET':
            autor = await autor_controller.get_one_crud(id_obj=autor_id)

            if not autor:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

            # Todas as tags disponíveis
            tags = await autor_controller.get_tags()

            # IDs das tags que o autor já possui
            tags_list = [tag.id for tag in autor.tags] if autor.tags else []

            context = {
                'request': request,
                'ano': datetime.now().year,
                'object': autor,
                'tags': tags,
                'tags_list': tags_list
            }

            return settings.TEMPLATES.TemplateResponse("admin/autor/edit.html", context=context)
        
        #Se o request for POST
        autor = await autor_controller.get_one_crud(id_obj=autor_id)

        if not autor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        #Recebe os dados do formulário e edita o autor
        form = await request.form()
        dados: set = None

        try:
            await autor_controller.put_crud(obj=autor)
        except ValueError as err:
            nome: str = form.get('nome')
            tags: List[str] = form.getlist('tag')
            dados = {"nome": nome, "tags": tags}
            context = {'request': request, "ano": datetime.now().year, 'error': err, 'objeto': dados}
            return settings.TEMPLATES.TemplateResponse(f"admin/autor/edit.html", context=context)
        
        return RedirectResponse(request.url_for("autor_list"), status_code=status.HTTP_302_FOUND)
    
autor_admin = AutorAdmin()