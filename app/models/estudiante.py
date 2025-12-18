from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class Estudiante(Base):
    __tablename__ = "estudiante"

    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), primary_key=True)
    institucion = Column(String(150), nullable=False)

    usuario = relationship("Usuario", back_populates="estudiante")
