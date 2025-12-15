# app/models/docente.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Docente(Base):
    __tablename__ = "docentes"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True)

    especialidad = Column(String(150), nullable=True)

    usuario = relationship("Usuario", back_populates="docente")
