from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Enum, ForeignKey, DateTime
)
from sqlalchemy.sql import func
from app.database.base import Base

class Leccion(Base):
    __tablename__ = "lecciones"

    id_leccion = Column(Integer, primary_key=True, index=True)

    id_area = Column(
        Integer,
        ForeignKey("areas.id_area"),
        nullable=False
    )

    titulo = Column(String(150), nullable=False)

    descripcion = Column(Text)

    nivel_recomendado = Column(
        Enum("Bajo", "Medio", "Alto", name="nivel_recomendado_enum"),
        nullable=False
    )

    activa = Column(Boolean, default=True)

    creado_por = Column(
        Integer,
        ForeignKey("usuario.id_usuario"),
        nullable=False
    )

    actualizado_por = Column(
        Integer,
        ForeignKey("usuario.id_usuario"),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )
