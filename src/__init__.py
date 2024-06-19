from fastapi import APIRouter, FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .models.User import Base
from .database.db import SessionLocal, engine, get_db
from .schemas import livro_schema, user_schema
from .services import crud_service
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.utils.util import get_flashed_messages
from src.views.user_router import user_router
from src.views.routes import root
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
from os import environ

load_dotenv()
# Configuração do banco de dados
Base.metadata.create_all(bind=engine)

# Instanciação da aplicação FastAPI
app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="$2y$10$tK0S7ttrqIZ3S1H26K31Q.ZCYoSABuzAE1cB75Iz6DLJ/LKsG7MBa", session_cookie="access_token")

# Configuração de arquivos estáticos
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# Configuração de templates com JINJA2
templates = Jinja2Templates(directory="src/templates")

# Registra o roteador de usuário
app.include_router(user_router)
app.include_router(root)

templates.env.globals["get_flashed_messages"] = get_flashed_messages

# Importação de rotas
from src.views import routes