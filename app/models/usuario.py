# app/models/usuario.py
from sqlalchemy import Column, Integer, String, Date, Enum
from sqlalchemy.orm import relationship
import enum

from app.database import Base


class TipoDocumento(enum.Enum):
    CC = "CC"
    CE = "CE"
    TI = "TI"


class RolUsuario(enum.Enum):
    ADMIN = "admin"
    ESTUDIANTE = "estudiante"
    DOCENTE = "docente"
    COORDINADOR = "coordinador"


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)

    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)

    tipo_documento = Column(Enum(TipoDocumento), nullable=False)
    documento = Column(String(30), unique=True, nullable=False)

    correo = Column(String(150), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)

    rol = Column(Enum(RolUsuario), nullable=False)

    fecha_nacimiento = Column(Date, nullable=False)

    # Relaciones 1 a 1
    estudiante = relationship("Estudiante", back_populates="usuario", uselist=False)
    docente = relationship("Docente", back_populates="usuario", uselist=False)
    coordinador = relationship("Coordinador", back_populates="usuario", uselist=False)
    admin = relationship("Admin", back_populates="usuario", uselist=False)
