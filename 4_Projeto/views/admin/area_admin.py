from datetime import datetime

from fastapi.routing import APIRouter
#Montar as rotas manualmente
from starlette.routing import Route

from fastapi import status
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse
from fastapi.exceptions import HTTPException

from core.configs import settings
from controllers.area_controller import AreaController
from views.admin.base_crud_view import BaseCRUDView


class AreaAdmin(BaseCRUDView):

    def __init__(self) -> None:
        self.router = APIRouter()

        self.router.routes.append(Route(path='/area/list', endpoint=self.object_list, methods=["GET"], name="area_list"))
        self.router.routes.append(Route(path='/area/create', endpoint=self.object_create, methods=["GET", "POST"], name="area_create"))
        self.router.routes.append(Route(path='/area/details/{area_id:int}', endpoint=self.object_edit, methods=["GET"], name="area_details"))
        self.router.routes.append(Route(path='/area/edit/{area_id:int}', endpoint=self.object_edit, methods=["GET", "POST"], name="area_edit"))
        self.router.routes.append(Route(path='/area/delete/{area_id:int}', endpoint=self.object_delete, methods=["GET", "DELETE"], name="area_delete"))

        super().__init__('area')

    #Implementa o método
    async def object_list(self, request: Request) -> Response:
        """ Rota para listar as áreas """
        #Instancia o controller
        area_controller = AreaController(request)

        #Passa o controller para o método da superclasse
        return await super().object_list(object_controller=area_controller)
    
    #Implementa o método
    async def object_delete(self, request: Request) -> Response:
        """ Rota para deletar uma área """
        area_controller: AreaController = AreaController(request)

        area_id: int = request.path_params['area_id']
        return await super().object_delete(object_controller=area_controller, obj_id=area_id)
    
    #Implementa o método
    async def object_create(self, request: Request) -> Response:
        """ Rota para criar uma área """
        area_controller: AreaController = AreaController(request)

        #Se o request for GET
        if request.method == 'GET':
            #Adicionar o request no contexto
            context = {'request': area_controller.request, "ano": datetime.now().year}

            return settings.TEMPLATES.TemplateResponse(f"admin/area/create.html", context=context)
        
        #Se o request for POST
        #Recebe os dados do formulário e cria a área
        try:
            await area_controller.post_crud()
            #Redireciona para a lista de áreas
        except ValueError as err:
            area: str = request.form().get('area')
            dados: set = { "area": area }
            context = {'request': request, "ano": datetime.now().year, "erro": err, "objeto": dados}
            return settings.TEMPLATES.TemplateResponse(f"admin/area/create.html", context=context)
        
        return RedirectResponse(request.url_for('area_list'), status_code=status.HTTP_302_FOUND)
    
    #Implementa o método
    async def object_edit(self, request: Request) -> Response:
        """ Rota para carregar o template e editar uma área """

        area_controller: AreaController = AreaController(request)
        area_id: int = request.path_params['area_id']

        #Se o request for GET
        if request.method == 'GET':
            return await super().object_edit(object_controller=area_controller, obj_id=area_id)
        
        #Se o request for POST
        area = await area_controller.get_one_crud(id_obj=area_id)

        if not area:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        #Recebe os dados do formulário e edita a área
        form = await request.form()
        dados: set = None

        try:
            await area_controller.put_crud(obj=area)
        except ValueError as err:
            area: str = form.get('area')
            dados: set = { "area": area }
            context = {'request': request, "ano": datetime.now().year, "erro": err, "objeto": dados}
            return settings.TEMPLATES.TemplateResponse(f"admin/area/edit.html", context=context)
        
        return RedirectResponse(request.url_for('area_list'), status_code=status.HTTP_302_FOUND)

area_admin = AreaAdmin()