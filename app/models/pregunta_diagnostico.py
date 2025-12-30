from sqlalchemy import (
    Column, Integer, String, Boolean,
    ForeignKey, Text, Enum, JSON
)
from sqlalchemy.orm import relationship
from app.database.database import Base


class PreguntaDiagnostico(Base):
    __tablename__ = "pregunta_diagnostico"

    id_pregunta_diagnostico = Column(Integer, primary_key=True)

    # =====================
    # RELACIONES
    # =====================
    test_id = Column(Integer, ForeignKey("test.id_test"), nullable=False)
    area_id = Column(Integer, ForeignKey("areas.id_area"), nullable=False)
    tipo_pregunta_id = Column(Integer, ForeignKey("tipo_pregunta.id_tipo_pregunta"), nullable=False)

    # =====================
    # CONTENIDO
    # =====================
    imagen_url = Column(String(255), nullable=True)
    contexto = Column(Text, nullable=True)
    enunciado = Column(Text, nullable=False)
    opciones = Column(JSON, nullable=True)
    respuesta_correcta = Column(Integer, nullable=True)

    dificultad = Column(Enum("Baja", "Media", "Alta"), nullable=False)
    activa = Column(Boolean, default=True)

    # =====================
    # ORM
    # =====================
    test = relationship("Test", back_populates="preguntas")
    area = relationship("Area", back_populates="preguntas")
    tipo_pregunta = relationship("TipoPregunta", back_populates="preguntas")
