from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.models.area import Area
from app.core.templates import templates
from app.database.database import get_db
from app.core.auth.dependencies import get_current_user

from app.schemas.pregunta_diagnostico import PreguntaDiagnosticoCreate
from app.models.pregunta_diagnostico import PreguntaDiagnostico

router = APIRouter(tags=["Admin"])


# =========================================================
# CATÁLOGO PRINCIPAL
# =========================================================
@router.get("/catalogo-contenidos", response_class=HTMLResponse)
def catalogo_contenidos(request: Request):
    areas = [
        {"nombre": "Matemáticas", "slug": "matematicas", "icono": "📐", "descripcion": "Pensamiento matemático"},
        {"nombre": "Lectura Crítica", "slug": "lectura-critica", "icono": "📘", "descripcion": "Comprensión de textos"},
        {"nombre": "Ciencias Naturales", "slug": "ciencias-naturales", "icono": "🧪", "descripcion": "Ciencia aplicada"},
        {"nombre": "Sociales y Ciudadanas", "slug": "sociales", "icono": "🌎", "descripcion": "Ciudadanía"},
        {"nombre": "Inglés", "slug": "ingles", "icono": "🇬🇧", "descripcion": "Reading"},
        {"nombre": "Destrezas Socio-Ocupacionales", "slug": "socio-ocupacional", "icono": "🧑‍💼", "descripcion": "Habilidades"},
        {
            "nombre": "Test diagnóstico breve",
            "slug": "test-diagnostico",
            "icono": "🧠",
            "descripcion": "Evaluación inicial para determinar el nivel académico",
            "destacado": True
        }
    ]

    return templates.TemplateResponse(
        "admin/formularios/index.html",
        {"request": request, "areas": areas}
    )


# =========================================================
# TEST DIAGNÓSTICO - HOME
# =========================================================
@router.get("/catalogo/test-diagnostico", response_class=HTMLResponse)
def test_diagnostico_home(request: Request):
    test_info = {
        "estado": "Activo",
        "duracion": "20 minutos",
        "preguntas": 20,
        "tipo": "Mixto",
        "intentos": 1
    }

    return templates.TemplateResponse(
        "admin/formularios/test_diagnostico/index.html",
        {"request": request, "test": test_info}
    )


# =========================================================
# TEST DIAGNÓSTICO - CONFIGURACIÓN
# =========================================================
@router.get("/catalogo/test-diagnostico/config", response_class=HTMLResponse)
def test_diagnostico_config(request: Request):
    config = {
        "tipo": "Mixto (todas las áreas)",
        "duracion": 20,
        "preguntas": 20,
        "intentos": 1,
        "mostrar_resultados": True,
        "uso_resultado": "Orientación académica",
        "estado": "Activo"
    }

    return templates.TemplateResponse(
        "admin/formularios/test_diagnostico/config.html",
        {
            "request": request,
            "config": config
        }
    )


# =========================================================
# TEST DIAGNÓSTICO - LISTAR PREGUNTAS (DESDE BD)
# =========================================================
@router.get(
    "/catalogo/test-diagnostico/preguntas",
    response_class=HTMLResponse
)
def listar_preguntas_diagnostico(
    request: Request,
    db: Session = Depends(get_db)
):
    preguntas = db.query(PreguntaDiagnostico).all()

    return templates.TemplateResponse(
        "admin/formularios/test_diagnostico/preguntas.html",
        {
            "request": request,
            "preguntas": preguntas
        }
    )


# =========================================================
# API - CREAR PREGUNTA DIAGNÓSTICO
# =========================================================
@router.post("/catalogo/test-diagnostico/preguntas")
def crear_pregunta_diagnostico(
    data: PreguntaDiagnosticoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    # Seguridad extra
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")

    # Validaciones básicas
    if len(data.opciones) < 2:
        raise HTTPException(
            status_code=400,
            detail="La pregunta debe tener al menos 2 opciones"
        )

    if data.respuesta_correcta >= len(data.opciones):
        raise HTTPException(
            status_code=400,
            detail="La respuesta correcta no es válida"
        )

    pregunta = PreguntaDiagnostico(
        id_area=data.id_area,
        dificultad=data.dificultad,
        enunciado=data.enunciado,
        opciones=data.opciones,
        respuesta_correcta=data.respuesta_correcta,
        activa=data.activa,
        creado_por=usuario.id_usuario
    )

    db.add(pregunta)
    db.commit()
    db.refresh(pregunta)

    return {
        "message": "Pregunta creada correctamente",
        "id_pregunta_diagnostico": pregunta.id_pregunta_diagnostico
    }


@router.get(
    "/catalogo/test-diagnostico/preguntas/nueva",
    response_class=HTMLResponse
)
def formulario_crear_pregunta(
    request: Request,
    db: Session = Depends(get_db)
):
    areas = db.query(Area).filter(Area.activa == True).all()

    return templates.TemplateResponse(
        "admin/formularios/test_diagnostico/editor.html",
        {
            "request": request,
            "areas": areas
        }
    )
