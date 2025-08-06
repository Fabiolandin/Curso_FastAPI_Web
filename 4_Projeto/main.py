from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request

#Configuração do FastAPI, desabilitando a documentação automática
app = FastAPI(docs_url=None, redoc_url=None)
templates = Jinja2Templates(directory="templates")

#Definindo o diretório para arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

#Criando rota index
@app.get('/', name="index")
async def index(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse('home/index.html', context=context)

#Criando rota about
@app.get('/about', name="about")
async def about(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse('about/about.html', context=context)

#Criando rota contact
@app.get('/contact', name="contact")
async def contact(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse('contact/contact.html', context=context)

#Criando rota pricing
@app.get('/pricing', name="pricing")
async def pricing(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse('pricing/pricing.html', context=context)

#Criando rota faq
@app.get('/faq', name="faq")
async def faq(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse('faq/faq.html', context=context)

#Criando rota blog_home
@app.get('/blog_home', name="blog_home")
async def blog_home(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse('blog_home/blog_home.html', context=context)

#Criando rota blog_post
@app.get('/blog_post', name="blog_post")
async def blog_post(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse('blog_post/blog_post.html', context=context)

#Criando rota portifolio_over
@app.get('/portifolio_over', name="portifolio_over")
async def portifolio_over(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse('portifolio_over/portifolio_over.html', context=context)

#Criando rota portifolio_item
@app.get('/portifolio_item', name="portifolio_item")
async def portifolio_item(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse('portifolio_item/portifolio_item.html', context=context)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, log_level="info", debug=True)