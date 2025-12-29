from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database.database import Base

class Area(Base):
    __tablename__ = "areas"

    id_area = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    codigo = Column(String(20), nullable=False)
    activa = Column(Boolean, default=True)

    # 👇 ESTO ES OBLIGATORIO
    preguntas = relationship(
        "PreguntaDiagnostico",
        back_populates="area"
    )

