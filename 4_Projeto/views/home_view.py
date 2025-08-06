from fastapi.routing import APIRouter
from fastapi.requests import Request

from core.configs import settings

router = APIRouter()

#Criando rota index
@router.get('/', name="index")
async def index(request: Request):
    context = {
        "request": request
    }
    return settings.TEMPLATES.TemplateResponse('home/index.html', context=context)

#Criando rota about
@router.get('/about', name="about")
async def about(request: Request):
    context = {
        "request": request
    }
    return settings.TEMPLATES.TemplateResponse('about/about.html', context=context)

#Criando rota contact
@router.get('/contact', name="contact")
async def contact(request: Request):
    context = {
        "request": request
    }
    return settings.TEMPLATES.TemplateResponse('contact/contact.html', context=context)

#Criando rota pricing
@router.get('/pricing', name="pricing")
async def pricing(request: Request):
    context = {
        "request": request
    }
    return settings.TEMPLATES.TemplateResponse('pricing/pricing.html', context=context)

#Criando rota faq
@router.get('/faq', name="faq")
async def faq(request: Request):
    context = {
        "request": request
    }
    return settings.TEMPLATES.TemplateResponse('faq/faq.html', context=context)

#Criando rota blog_home
@router.get('/blog_home', name="blog_home")
async def blog_home(request: Request):
    context = {
        "request": request
    }
    return settings.TEMPLATES.TemplateResponse('blog_home/blog_home.html', context=context)

#Criando rota blog_post
@router.get('/blog_post', name="blog_post")
async def blog_post(request: Request):
    context = {
        "request": request
    }
    return settings.TEMPLATES.TemplateResponse('blog_post/blog_post.html', context=context)

#Criando rota portifolio_over
@router.get('/portifolio_over', name="portifolio_over")
async def portifolio_over(request: Request):
    context = {
        "request": request
    }
    return settings.TEMPLATES.TemplateResponse('portifolio_over/portifolio_over.html', context=context)

#Criando rota portifolio_item
@router.get('/portifolio_item', name="portifolio_item")
async def portifolio_item(request: Request):
    context = {
        "request": request
    }
    return settings.TEMPLATES.TemplateResponse('portifolio_item/portifolio_item.html', context=context)
