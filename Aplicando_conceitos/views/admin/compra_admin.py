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
from controllers.compra_controller import CompraController
from views.admin.base_crud_view import BaseCRUDView

class CompraAdmin(BaseCRUDView):
    def __init__(self) -> None:
        self.router = APIRouter()

        self.router.routes.append(Route(path='/compra/list', endpoint=self.object_list, methods=["GET"], name="compra_list"))
        self.router.routes.append(Route(path='/compra/create', endpoint=self.object_create, methods=["GET", "POST"], name="compra_create"))
        self.router.routes.append(Route(path='/compra/details/{compra_id:int}', endpoint=self.object_edit, methods=["GET"], name="compra_details"))
        self.router.routes.append(Route(path='/compra/edit/{compra_id:int}', endpoint=self.object_edit, methods=["GET", "POST"], name="compra_edit"))
        self.router.routes.append(Route(path='/compra/delete/{compra_id:int}', endpoint=self.object_delete, methods=["GET", "DELETE"], name="compra_delete"))

        super().__init__('compra')

    #Implementação do método list
    async def object_list(self, request: Request) -> Response:
        """ Rota para listar as compras """
        #Instancia o controller
        compra_controller = CompraController(request)

        #Passa o controller para o método da superclasse
        return await super().object_list(object_controller=compra_controller)

    #Implementação do método delete
    async def object_delete(self, request: Request) -> Response:
        """ Rota para deletar uma compra """
        compra_controller: CompraController = CompraController(request)

        compra_id: int = request.path_params['compra_id']
        return await super().object_delete(object_controller=compra_controller, obj_id=compra_id)

    #Implementação do método create
    async def object_create(self, request: Request) -> Response:
        """ Rota para criar uma compra """
        compra_controller: CompraController = CompraController(request)

        #Se o request for GET
        if request.method == "GET":
            #Adicionar o request no contexto e as listas necessárias
            fornecedores = await compra_controller.get_fornecedores()
            funcionarios = await compra_controller.get_funcionarios()
            produtos = await compra_controller.get_produtos()
            
            context = {
                'request': compra_controller.request, 
                "ano": datetime.now().year, 
                "fornecedores": fornecedores, 
                "funcionarios": funcionarios,
                "produtos": produtos
            }

            return settings.TEMPLATES.TemplateResponse(f"admin/compra/create.html", context=context)
        
        #Se o request for POST
        #Recebe os dados do formulário e cria a compra
        
        try:
            await compra_controller.post_crud()
        except ValueError as err:
            # Em caso de erro, re-renderizar para o usuário não perder tudo (Melhoria futura: manter dados já preenchidos)
            # Por enquanto, apenas recarregar as listas e mostrar erro
            fornecedores = await compra_controller.get_fornecedores()
            funcionarios = await compra_controller.get_funcionarios()
            produtos = await compra_controller.get_produtos()
            
            context = {
                'request': request, 
                "ano": datetime.now().year, 
                "error": err, 
                "fornecedores": fornecedores, 
                "funcionarios": funcionarios,
                "produtos": produtos
            }
            return settings.TEMPLATES.TemplateResponse(f"admin/compra/create.html", context=context)
        
        return RedirectResponse(request.url_for('compra_list'), status_code=status.HTTP_302_FOUND)

    #Implementação do método edit
    async def object_edit(self, request: Request) -> Response:
        """ Rota para editar uma compra """
        compra_controller: CompraController = CompraController(request)
        compra_id: int = request.path_params['compra_id']

        #Se o request for GET
        if request.method == "GET":
            if 'details' in str(request.url):
                return await super().object_details(object_controller=compra_controller, obj_id=compra_id)

            compra = await compra_controller.get_one_crud(id_obj=compra_id)
            
            if not compra:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            
            # Dados para o formulário
            fornecedores = await compra_controller.get_fornecedores()
            funcionarios = await compra_controller.get_funcionarios()

            context = {
                'request': request,
                'ano': datetime.now().year,
                'object': compra,
                'categorias': { 'fornecedores': fornecedores, 'funcionarios': funcionarios } # Passing as 'categorias' to match my template hack or better rename in template? 
                # Actually, better to pass clean context keys and update template to match.
                # But my template used "categorias.fornecedores". I should probably stick to that or update template.
                # Let's update the template to use "fornecedores" and "funcionarios" directly?
                # No, I already wrote the template in the previous step using "categorias.fornecedores". 
                # Wait, in the previous step I WROTE: {% for f in categorias.fornecedores %}
                # So I must pass a dictionary named 'categorias' or update the template.
                # I'll pass clean keys here and UPDATE the template in the next step to be clean, OR just pass clean keys and trust I'll fix the template?
                # Actually, I haven't written the template to disk yet? No, I did.
                # It's better to update the template to use 'fornecedores' directly.
            }
            # Wait, let's look at what I wrote in edit.html:
            # {% for f in categorias.fornecedores %}
            # I should fix the Python to pass it cleanly and fix the template.
            # actually, passing "fornecedores": fornecedores is standard. I'll do that.

            context = {
                'request': request,
                'ano': datetime.now().year,
                'object': compra,
                'fornecedores': fornecedores,
                'funcionarios': funcionarios
            }

            return settings.TEMPLATES.TemplateResponse("admin/compra/edit.html", context=context)
        
        #Se o request for POST
        compra = await compra_controller.get_one_crud(id_obj=compra_id)

        if not compra:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        #Recebe os dados do formulário e edita a compra
        form = await request.form()
        dados: set = None

        try:
            await compra_controller.put_crud(obj=compra)
        except ValueError as err:
            nome: str = form.get('nome')
            categorias: List[str] = form.getlist('categoria')
            dados = { "nome": nome, "categorias": categorias}
            context = {'request': request, "ano": datetime.now().year, 'error': err, 'objeto': dados}
            return settings.TEMPLATES.TemplateResponse(f"admin/compra/edit.html", context=context)
        
        return RedirectResponse(request.url_for("compra_list"), status_code=status.HTTP_302_FOUND)

compra_admin = CompraAdmin()
