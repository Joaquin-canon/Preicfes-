from fastapi import APIRouter

router = APIRouter(
    prefix="/preguntas",
    tags=["Preguntas ICFES"]
)

@router.get("/")
def obtener_preguntas():
    return [
        {
            "id": 1,
            "asignatura": "Matemáticas",
            "pregunta": "¿Cuánto es 2 + 2?",
            "opciones": ["2", "3", "4", "5"],
            "respuesta": "4"
        }
    ]
