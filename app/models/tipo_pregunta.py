from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from app.database.database import Base
from sqlalchemy.orm import relationship
class TipoPregunta(Base):
    __tablename__ = "tipo_pregunta"

    id_tipo_pregunta = Column(Integer, primary_key=True)
    codigo = Column(String(30), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String)
    activa = Column(Boolean, default=True)

    preguntas = relationship(
        "PreguntaDiagnostico",
        back_populates="tipo_pregunta"
    )
