from pydantic import BaseModel
from typing import List

class PreguntaDiagnosticoCreate(BaseModel):
    id_area: int
    dificultad: str
    enunciado: str
    opciones: List[str]
    respuesta_correcta: int
    activa: bool = True
