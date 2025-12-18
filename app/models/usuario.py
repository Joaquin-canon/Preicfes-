from sqlalchemy import Column, Integer, String, Enum, Date, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database.database import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    tipo_documento = Column(Enum("CC", "CE", "TI"), nullable=False)
    numero_documento = Column(String(20), unique=True, nullable=False)
    correo = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    rol = Column(Enum("estudiante", "docente", "coordinador", "admin"), nullable=False)
    activo = Column(Boolean, default=True)

    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    # Relaciones 1–1 por rol
    admin = relationship("Admin", back_populates="usuario", uselist=False)
    docente = relationship("Docente", back_populates="usuario", uselist=False)
    coordinador = relationship("Coordinador", back_populates="usuario", uselist=False)
    estudiante = relationship("Estudiante", back_populates="usuario", uselist=False)
