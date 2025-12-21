from sqlalchemy import Column, Integer, String, Boolean
from app.database.database import Base

class Area(Base):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    codigo = Column(String(30), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    activa = Column(Boolean, default=True)
