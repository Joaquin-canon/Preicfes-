from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class Coordinador(Base):
    __tablename__ = "coordinador"

    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), primary_key=True)

    usuario = relationship("Usuario", back_populates="coordinador")
