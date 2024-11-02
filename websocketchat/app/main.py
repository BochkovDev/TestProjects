from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from core.jinja2 import templates
from core.settings import settings
from users.router import router as router_users
from chat.router import router as router_chat


app = FastAPI()
app.mount('/static', StaticFiles(directory=settings.STATIC_DIR), name='static')


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'], 
    allow_credentials=True,
    allow_methods=['*'],  
    allow_headers=['*'],  
)


@app.get('/', response_class=HTMLResponse, summary='Страница авторизации и регистрации')
async def root(request: Request):
    return templates.TemplateResponse('auth.html', {'request': request})


app.include_router(router_users)
app.include_router(router_chat)