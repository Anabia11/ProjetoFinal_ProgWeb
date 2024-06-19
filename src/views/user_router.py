from fastapi import FastAPI, Depends, HTTPException, Request, Form, UploadFile, File, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from src.schemas import user_schema
from src.services import crud_service
from src.utils.util import flash, verify_password
from sqlalchemy.orm import Session
from src.database.db import get_db
from fastapi import Depends

# Jinja2Templates
templates = Jinja2Templates(directory="src/templates")

# APIRouter para organizar rotas de usuario
user_router = APIRouter(
    prefix="/usuario",
    tags=["usuario"],
    responses={404: {"description": "Not found"}},
)

# Método GET para renderizar pagina de cadastro
@user_router.get('/cadastro')
async def cadastro_user(request: Request):
    return templates.TemplateResponse("cadastro/cadastrar_user.html", {"request": request})

# Método POST para cadastrar usuario
@user_router.post('/cadastrar')
async def cadastrar_user(request: Request, db: Session = Depends(get_db), user: str = Form(...), email: str = Form(...), password: str = Form(...)):
    # Validação básica
    existing_user = crud_service.get_user_by_email(db, email)
    if existing_user:
        flash(request, "Este email já está cadastrado. Por favor, use outro email.", "red")
        return templates.TemplateResponse("cadastro/cadastrar_user.html", {"request": request})

    # Criação do schema de usuário
    data_user = user_schema.UserCreate(
        nome=user, email=email, password=password)

    # Tentativa de criar o usuário no banco de dados
    try:
        db_user = crud_service.create_user(db=db, user=data_user)
    except Exception as e:
        # Log do erro para debug (opcional)
        print(f"Erro ao criar usuário: {e}")
        flash(request, "Houve um erro ao cadastrar usuário. Tente novamente ou contate um administrador.", "red")
        return templates.TemplateResponse("cadastro/cadastrar_user.html", {"request": request})

    # Se o usuário foi criado com sucesso, redirecionar para a página inicial
    if db_user:
        flash(request, "Usuário cadastrado com sucesso!", "green")
        return RedirectResponse("/usuario/login", status_code=303)
    else:
        flash(request, "Houve um erro ao cadastrar usuário. Tente novamente ou contate um administrador.", "red")
        return templates.TemplateResponse("cadastro/cadastrar_user.html", {"request": request})

# Método GET para renderizar html de login
@user_router.get('/login')
async def cadastro_user(request: Request):
    return templates.TemplateResponse("cadastro/login_user.html", {"request": request})

# Método POST para logar usuario
@user_router.post('/logar')
async def logar_user(request: Request, response: Response, db: Session = Depends(get_db), email: str = Form(...), password: str = Form(...)):
    # Capturando usuario no banco de dados
    db_user = crud_service.get_user_by_email(db, email)

    # Verifica se o usuário existe no banco de dados
    if not db_user:
        flash(request, "Credenciais inválidas. Verifique seu email e senha!", "red")
        return templates.TemplateResponse("cadastro/login_user.html", {"request": request})

    # Verifica se o usuário existe no banco de dados
    if not verify_password(password, db_user.hashed_password):
        flash(request, "Credenciais inválidas. Verifique seu email e senha!", "red")
        return templates.TemplateResponse("cadastro/login_user.html", {"request": request})

    flash(request, f"Usuario {db_user.nome} logado com sucesso!", "blue")

    # Redirecionamento para pagina principal
    return RedirectResponse("/", status_code=303)
