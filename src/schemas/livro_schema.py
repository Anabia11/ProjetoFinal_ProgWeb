from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date

class LivroBase(BaseModel):
    """
    Classe base para representar os dados básicos de um livro.

    Atributos:
    - titulo (str): Título do livro.
    - autor (str): Autor do livro.
    - editora (Optional[str]): Editora do livro (opcional).
    - idioma (Optional[str]): Idioma do livro (opcional).
    - sinopse (Optional[str]): Sinopse do livro (opcional).
    - imagem (Optional[str]): URL da imagem do livro (opcional).
    """
    titulo: str
    autor: str
    editora: Optional[str] = None
    idioma: Optional[str] = None
    sinopse: Optional[str] = None
    imagem: Optional[bytes] = None 
    imagem_tipo: Optional[str] = None

class LivroCreate(LivroBase):
    """
    Classe para representar os dados necessários para criar um novo livro.

    Herança:
    - LivroBase: Herda todos os atributos da classe base LivroBase.
    """
    pass

class Livro(LivroBase):
    """
    Classe para representar um livro completo, incluindo identificador, timestamps e ID do usuário.

    Herança:
    - LivroBase: Herda todos os atributos da classe base LivroBase.

    Atributos adicionais:
    - id (int): Identificador único do livro.
    - user_id (int): Identificador único do usuário proprietário do livro.
    - data_criacao (datetime): Data e hora de criação do livro (padrão para datetime.now()).
    - data_atualizacao (datetime): Data e hora da última atualização do livro (padrão para datetime.now()).

    Configuração:
    - Config.from_attributes = True: Permite a criação da instância usando atributos nomeados.
    """
    id: int
    user_id: int
    data_criacao: datetime = Field(default_factory=datetime.now)
    data_atualizacao: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True
