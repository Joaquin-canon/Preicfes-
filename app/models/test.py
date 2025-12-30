from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from app.database.database import Base
from sqlalchemy.sql import func


class Test(Base):
    __tablename__ = "test"

    id_test = Column(Integer, primary_key=True, index=True)
    slug = Column(String(50), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)

    activo = Column(Boolean, default=True)

    duracion_minutos = Column(Integer, nullable=False)
    numero_preguntas = Column(Integer, nullable=False)
    numero_intentos = Column(Integer, nullable=False, default=1)

    mostrar_resultado = Column(Boolean, default=True)
    mostrar_respuestas = Column(Boolean, default=False)
    aleatorizar_preguntas = Column(Boolean, default=True)
    aleatorizar_opciones = Column(Boolean, default=True)

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    preguntas = relationship(
        "PreguntaDiagnostico",
        back_populates="test",
        cascade="all, delete-orphan"
    )
