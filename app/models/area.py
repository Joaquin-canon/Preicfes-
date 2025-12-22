# app/models/area.py

from sqlalchemy import Column, Integer, String, Boolean
from app.database.database import Base

class Area(Base):
    __tablename__ = "areas"

    id_area = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    codigo = Column(String(20), nullable=False)
    activa = Column(Boolean, default=True)
