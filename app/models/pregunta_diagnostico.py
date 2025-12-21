from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.types import JSON
from app.database.database import Base

class PreguntaDiagnostico(Base):
    __tablename__ = "pregunta_diagnostico"

    id = Column(Integer, primary_key=True)

    area_id = Column(Integer, ForeignKey("areas.id_area"), nullable=False)
    tipo_pregunta_codigo = Column(String(20), nullable=False)

    dificultad = Column(Enum("Baja", "Media", "Alta"), nullable=False)
    enunciado = Column(String(500), nullable=False)

    opciones = Column(JSON, nullable=False)
    respuesta_correcta = Column(Integer, nullable=False)

    activa = Column(Boolean, default=True)
    creado_por = Column(Integer, ForeignKey("usuario.id_usuario"))
