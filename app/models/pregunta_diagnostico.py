from sqlalchemy import (
    Column, Integer, Text, Boolean, Enum, ForeignKey, JSON, DateTime
)
from sqlalchemy.sql import func
from app.database.base import Base

class PreguntaDiagnostico(Base):
    __tablename__ = "pregunta_diagnostico"

    id_pregunta_diagnostico = Column(
        Integer, primary_key=True, index=True
    )

    id_area = Column(
        Integer,
        ForeignKey("areas.id_area"),
        nullable=False
    )

    dificultad = Column(
        Enum("Baja", "Media", "Alta", name="dificultad_enum"),
        nullable=False
    )

    enunciado = Column(Text, nullable=False)

    opciones = Column(JSON, nullable=False)

    respuesta_correcta = Column(Integer, nullable=False)

    activa = Column(Boolean, default=True)

    creado_por = Column(
        Integer,
        ForeignKey("usuario.id_usuario"),
        nullable=False
    )

    actualizado_por = Column(
        Integer,
        ForeignKey("usuario.id_usuario"),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )
