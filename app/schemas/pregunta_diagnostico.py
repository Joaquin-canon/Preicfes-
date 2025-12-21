from pydantic import BaseModel
from typing import List

class PreguntaDiagnosticoCreate(BaseModel):
    tipo_pregunta_codigo: str
    area_id: int
    dificultad: str
    enunciado: str
    opciones_json: str   # viene como JSON string
    respuesta_correcta: int
