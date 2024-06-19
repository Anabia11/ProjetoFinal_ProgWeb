from pydantic import BaseModel
from src.schemas.livro_schema import Livro  # Importa o modelo de livro
from typing import List

class UserBase(BaseModel):
    """
    Classe base para representar os dados básicos de um usuário.

    Atributos:
    - nome (str): Nome completo do usuário.
    - email (str): Endereço de e-mail do usuário.
    """
    nome: str
    email: str

class UserCreate(UserBase):
    """
    Classe para representar os dados necessários para criar um novo usuário.

    Herança:
    - UserBase: Herda todos os atributos da classe base UserBase.

    Atributos adicionais:
    - password (str): Senha do usuário para criação da conta.
    """
    password: str

class User(UserBase):
    """
    Classe para representar um usuário completo, incluindo identificador, status de ativação e lista de livros.

    Herança:
    - UserBase: Herda todos os atributos da classe base UserBase.

    Atributos adicionais:
    - id (int): Identificador único do usuário.
    - is_active (bool): Indica se o usuário está ativo ou não.
    - livros (List[Livro]): Lista de livros associados ao usuário (padrão para uma lista vazia).

    Configuração:
    - Config.from_attributes = True: Permite a criação da instância usando atributos nomeados.
    """
    id: int
    is_active: bool
    livros: List[Livro] = []  # Inicializa com uma lista vazia de livros

    class Config:
        from_attributes = True
