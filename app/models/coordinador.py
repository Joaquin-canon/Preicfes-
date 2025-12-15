# app/models/coordinador.py
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Coordinador(Base):
    __tablename__ = "coordinadores"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True)

    usuario = relationship("Usuario", back_populates="coordinador")
