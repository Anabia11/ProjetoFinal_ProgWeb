from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, LargeBinary
from sqlalchemy.orm import relationship
from datetime import datetime

from src.database.db import Base

class Livro(Base):
    __tablename__ = 'livros'

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False, index=True)
    autor = Column(String, nullable=False)
    editora = Column(String, nullable=False)
    idioma = Column(String, nullable=False)
    sinopse = Column(String, nullable=True)
    imagem = Column(LargeBinary, nullable=True)
    imagem_tipo = Column(String, nullable=True)
    data_criacao = Column(DateTime, default=datetime.now)
    data_atualizacao = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="livros")