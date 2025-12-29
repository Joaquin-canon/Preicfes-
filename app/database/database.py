from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base
from app.models.area import Area
from app.models.tipo_pregunta import TipoPregunta
from app.models.pregunta_diagnostico import PreguntaDiagnostico

DATABASE_URL = "mysql+pymysql://root@localhost/pre_icfes"


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
