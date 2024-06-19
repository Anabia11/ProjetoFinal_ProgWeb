from sqlalchemy.orm import Session
from src.models import Livro, User
from src.schemas import livro_schema, user_schema
from src.utils.util import hash_password


def get_user(db: Session, user_id: int):
    return db.query(User.User).filter(User.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User.User).filter(User.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: user_schema.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User.User(
        nome=user.nome,
        email=user.email,
        hashed_password=hashed_password
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Livro.Livro).offset(skip).limit(limit).all()


def create_book(db: Session, book: livro_schema.LivroCreate, user_id: int):
    db_book = Livro.Livro(
        titulo=book.titulo,
        autor=book.autor,
        editora=book.editora,
        idioma=book.idioma,
        sinopse=book.sinopse,
        imagem=book.imagem,
        imagem_tipo=book.imagem_tipo,
        user_id=user_id  # Relacionando o livro ao usuário
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book