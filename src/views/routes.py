from urllib import request
from fastapi import Cookie, FastAPI, Depends, HTTPException, Request, Form, UploadFile, File, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
import jwt
from sqlalchemy.orm import Session
from src.models.User import Base
from src.models import Livro
from src.database.db import SessionLocal, engine, get_db
from src.schemas import livro_schema, user_schema
from src.services import crud_service
from src.services.crud_service import get_books
from src.utils.util import flash
from src import templates
from fastapi.security import OAuth2PasswordBearer
from pathlib import Path
from typing import Annotated, Optional
from starlette import status
import shutil
import base64
import os

root = APIRouter()

UPLOAD_DIRECTORY = Path("src") / "static" / "uploads"
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)

templates = Jinja2Templates(directory="src/templates")

# Rota principal - HOME
@root.get('/', response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    select_books = get_books(db)

    return templates.TemplateResponse(
        "home.html",
        {"request": request, "books": select_books}
    )

# Rota de página de cadastro
@root.get('/cadastro', response_class=HTMLResponse)
async def cadastro(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='cadastro/cadastrar.html'
    )

# Método POST para cadastrar o livro
@root.post('/cadastrar')
async def cadastrar(request: Request, db: Session = Depends(get_db), title: str = Form(...), author: str = Form(...), company: str = Form(...), language: str = Form(...), description: str = Form(None), image: UploadFile = File(None)):
    if not all([title, author, company, language]):
        flash(request, "Por favor, preencha todos os campos.", "red")
        return templates.TemplateResponse(
            "edicao/editar.html", 
            {
                "request": request,
                "title": title,
                "author": author,
                "company": company,
                "language": language,
                "description": description,
                "error_message": "Por favor, preencha os campos corretamente."
            }
        )

    if not title.strip():
        flash(request, "Por favor, preencha os campos corretamente!", "red")
        return templates.TemplateResponse(
            "edicao/editar.html", 
            {
                "request": request,
                "title": title,
                "author": author,
                "company": company,
                "language": language,
                "description": description,
                "error_message": "Por favor, preencha os campos corretamente."
            }
        )

    image_path = None
    if image and image.filename:
        try:
            # image_path = UPLOAD_DIRECTORY / image.filename
            # with open(image_path, "wb") as buffer:
            #     shutil.copyfileobj(image.file, buffer)
            # book.imagem = f"uploads/{image.filename}"  # Atualiza o caminho da imagem
            image_bytes = await image.read() 
            imagem = image_bytes
            imagem_tipo = image.content_type
        except Exception as e:
            print(f'Erro ao fazer upload da imagem. {e}')
            raise HTTPException(status_code=500, detail="Erro ao fazer upload da imagem.")


    # print(image_path.absolute())
    data_book = livro_schema.LivroCreate(
        titulo=title,
        autor=author,
        editora=company,
        idioma=language,
        sinopse=description,
        imagem=imagem,
        imagem_tipo=imagem_tipo
    )

    db_book = crud_service.create_book(db=db, book=data_book, user_id=2)

    if db_book:
        # response = RedirectResponse("/", status_code=303)
        flash(request, "Livro adicionado com sucesso!", "success")
        return RedirectResponse("/", status_code=303)

    return {"message": "Houve um problema ao cadastrar o livro"}

# Método POST para DELETAR um livro
@root.post('/deletar/{book_id}', response_class=HTMLResponse)
async def delete(request: Request, book_id: int, db: Session = Depends(get_db)):
    try:
        book_to_delete = db.query(Livro.Livro).filter(Livro.Livro.id == book_id).first()

        if not book_to_delete:
            raise HTTPException(status_code=404, detail="Livro não encontrado")
        
        db.delete(book_to_delete)
        db.commit()
        flash(request, "Livro deletado com sucesso!", category="red")
    except Exception as e:  
        raise HTTPException(status_code=500, detail="Erro ao deletar livro")
    return RedirectResponse("/", status_code=303)

# Método GET para renderizar pagina de edicao
@root.get('/editar/{book_id}', response_class=HTMLResponse)
async def edit_book(request: Request, book_id: int, db: Session = Depends(get_db)):
    book = db.query(Livro.Livro).filter(Livro.Livro.id == book_id).first()
    if not book:
        raise HTTPException(404, "Livro não encontrado")
    
    return templates.TemplateResponse("edicao/editar.html", {"request": request, "book": book})

@root.get('/imagem/{book_id}')
async def get_image(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Livro.Livro).filter(Livro.Livro.id == book_id).first()
    if not book or not book.imagem:
        raise HTTPException(status_code=404, detail="Imagem não encontrada")
    
    return Response(content=book.imagem, media_type=book.imagem_tipo)

# Método POST para editar um livro
@root.post('/editar/{book_id}', response_class=HTMLResponse)
async def update_book(request: Request, book_id: int, db: Session = Depends(get_db), title: str = Form(...), author: str = Form(...), company: str = Form(...), language: str = Form(...), description: str = Form(None), image: UploadFile = File(None)):
    book = db.query(Livro.Livro).filter(Livro.Livro.id == book_id).first()
    if not book:
        raise HTTPException(404, "Livro não encontrado")

    if not title.strip():
        flash(request, "Por favor, preencha os campos corretamente!", "red")
        return templates.TemplateResponse(
            "edicao/editar.html", 
            {
                "request": request,
                "book": book,
                "title": title,
                "author": author,
                "company": company,
                "language": language,
                "description": description,
                "error_message": "Por favor, preencha os campos corretamente."
            }
        )

    book.titulo = title
    book.autor = author
    book.editora = company
    book.idioma = language
    book.sinopse = description

    if image and image.filename:
        try:
            # image_path = UPLOAD_DIRECTORY / image.filename
            # with open(image_path, "wb") as buffer:
            #     shutil.copyfileobj(image.file, buffer)
            # book.imagem = f"uploads/{image.filename}"  # Atualiza o caminho da imagem
            image_bytes = await image.read() 
            book.imagem = image_bytes
            book.imagem_tipo = image.content_type
        except Exception as e:
            print(f'Erro ao fazer upload da imagem. {e}')
            raise HTTPException(status_code=500, detail="Erro ao fazer upload da imagem.")

    try:
        db.commit()
        db.refresh(book)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao atualizar livro. Erro: {e}")

    flash(request, "Livro atualizado com sucesso!", "green")
    return RedirectResponse("/", status_code=303)
