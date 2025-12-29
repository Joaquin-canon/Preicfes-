from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.database import Base

from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from app.database.database import Base


class PreguntaDiagnostico(Base):
    __tablename__ = "pregunta_diagnostico"

    id_pregunta_diagnostico = Column(Integer, primary_key=True)

    area_id = Column(Integer, ForeignKey("areas.id_area"), nullable=False)
    tipo_pregunta_id = Column(Integer, ForeignKey("tipo_pregunta.id_tipo_pregunta"), nullable=False)

    dificultad = Column(Enum("Baja", "Media", "Alta"), nullable=False)
    contexto = Column(Text, nullable=True)
    enunciado = Column(Text, nullable=False)
    opciones = Column(JSON, nullable=True)
    respuesta_correcta = Column(Integer, nullable=True)
    activa = Column(Boolean, default=True)

    area = relationship("Area", back_populates="preguntas")
    tipo_pregunta = relationship("TipoPregunta", back_populates="preguntas")
