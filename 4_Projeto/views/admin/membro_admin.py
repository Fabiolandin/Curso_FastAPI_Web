from datetime import datetime

from fastapi.routing import APIRouter
from starlette.routing import Route
from fastapi import status
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse
from fastapi.exceptions import HTTPException

from core.configs import settings
from controllers.membro_controller import MembroController
from views.admin.base_crud_view import BaseCRUDView



class MembroAdmin(BaseCRUDView):

    def __init__(self) -> None:
        self.router = APIRouter()

        self.router.routes.append(Route(path='/membro/list', endpoint=self.object_list, methods=["GET"], name="membro_list"))
        self.router.routes.append(Route(path='/membro/create', endpoint=self.object_create, methods=["GET", "POST"], name="membro_create"))
        self.router.routes.append(Route(path='/membro/details/{membro_id: int}', endpoint=self.object_details, methods=["GET"], name="membro_details"))
        self.router.routes.append(Route(path='/membro/edit/{membro_id: int}', endpoint=self.object_edit, methods=["GET", "POST"], name="membro_edit"))
        self.router.routes.append(Route(path='/membro/delete/{membro_id: int}', endpoint=self.object_delete, methods=["DELETE"], name="membro_delete"))

        super().__init__('membros')

    
    async def object_list(self, request: Request) -> Response:
        """ Rota para listar os membros """
        membro_controller = MembroController(request)

        return await super().object_list(object_controller=membro_controller)
    
    
    async def object_delete(self, request: Request) -> Response:
        """ Rota para deletar um membro """
        membro_controller: MembroController = MembroController(request)

        membro_id: int = request.path_params['membro_id']
        return await super().object_delete(object_controller=membro_controller, obj_id=membro_id)
    
    
    async def object_create(self, request: Request) -> Response:
        """ Rota para criar um membro """
        membro_controller: MembroController = MembroController(request)

        if request.method == 'GET':
            #Adicionar o request no contexto
            

        return await super().object_create()