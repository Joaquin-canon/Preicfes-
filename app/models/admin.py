from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Admin(Base):
    __tablename__ = "admin"

    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), primary_key=True)

    usuario = relationship("Usuario", back_populates="admin")
