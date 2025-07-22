from fastapi import FastAPI
from fastapi.responses import HTMLResponse

#Instanciando FASTAPI e colocando na variavel APP
app = FastAPI()

#Decorador de rota: O @app.get define que esta função será chamada quando uma requisição HTTP GET for feita para ('/', que é a rota raiz).
@app.get('/')
async def index(): #Função Assíncrona
    conteudo = """
        <center>
            <h1> FASTAPI WEB </h1>
            <span> Para mais cursos, visite a GEEK University <a href="https://www.geekuniversity.com.br" target="_blank">aqui</a>.</span>
        <center>
"""
    return HTMLResponse(content=conteudo)

#Executa toda vez que o script for rodado
if __name__ == '__main__':
    import uvicorn #Importando o servidor que rodará a aplicação

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)