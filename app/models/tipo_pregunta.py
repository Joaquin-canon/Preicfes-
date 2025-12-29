from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database.database import Base

class TipoPregunta(Base):
    __tablename__ = "tipo_pregunta"

    id_tipo_pregunta = Column(Integer, primary_key=True)
    codigo = Column(String(50), nullable=False)
    nombre = Column(String(100), nullable=False)
    activa = Column(Boolean, default=True)

    preguntas = relationship(
        "PreguntaDiagnostico",
        back_populates="tipo_pregunta"
    )
