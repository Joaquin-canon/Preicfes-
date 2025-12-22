from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import json

from app.core.templates import templates
from app.database.database import get_db
from app.core.auth.dependencies import get_current_user
from fastapi.responses import HTMLResponse, RedirectResponse
from app.models.area import Area
from app.models.tipo_pregunta import TipoPregunta
from app.models.pregunta_diagnostico import PreguntaDiagnostico
from app.schemas.pregunta_diagnostico import PreguntaDiagnosticoCreate


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
        {"request": request, "config": config}
    )


# =========================================================
# TEST DIAGNÓSTICO - LISTAR PREGUNTAS (DESDE BD)
# =========================================================
@router.get("/catalogo/test-diagnostico/preguntas", response_class=HTMLResponse)
def listar_preguntas_diagnostico(
    request: Request,
    db: Session = Depends(get_db),
    page: int = 1,
    area_id: int | None = None,
    tipo_id: int | None = None,
    dificultad: str | None = None,
    estado: str | None = None,
    q: str | None = None,
):
    # 🔐 Seguridad MANUAL (HTML-friendly)
    try:
        usuario = get_current_user(request, db)
    except Exception:
        return RedirectResponse("/login", status_code=302)

    if usuario.rol != "admin":
        return RedirectResponse("/login", status_code=302)

    # -----------------------------
    # QUERY BASE
    # -----------------------------
    query = db.query(PreguntaDiagnostico)

    # -----------------------------
    # FILTROS
    # -----------------------------
    if area_id:
        query = query.filter(PreguntaDiagnostico.area_id == area_id)

    if tipo_id:
        query = query.filter(PreguntaDiagnostico.tipo_pregunta_id == tipo_id)

    if dificultad:
        query = query.filter(PreguntaDiagnostico.dificultad == dificultad)

    if estado == "activa":
        query = query.filter(PreguntaDiagnostico.activa == True)
    elif estado == "inactiva":
        query = query.filter(PreguntaDiagnostico.activa == False)

    if q:
        query = query.filter(PreguntaDiagnostico.enunciado.ilike(f"%{q}%"))

    # -----------------------------
    # PAGINACIÓN
    # -----------------------------
    page_size = 10
    total = query.count()
    total_pages = max((total + page_size - 1) // page_size, 1)

    preguntas = (
        query
        .order_by(PreguntaDiagnostico.id_pregunta_diagnostico.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    # -----------------------------
    # DATA AUXILIAR
    # -----------------------------
    areas = db.query(Area).filter(Area.activa == True).all()
    tipos_pregunta = db.query(TipoPregunta).filter(TipoPregunta.activa == True).all()

    return templates.TemplateResponse(
        "admin/formularios/test_diagnostico/banco_preguntas/preguntas.html",
        {
            "request": request,
            "preguntas": preguntas,
            "areas": areas,
            "tipos_pregunta": tipos_pregunta,
            "page": page,
            "total_pages": total_pages,
            "filters": {
                "area_id": area_id,
                "tipo_id": tipo_id,
                "dificultad": dificultad,
                "estado": estado,
                "q": q
            }
        }
    )


# =========================================================
# API - CREAR PREGUNTA DIAGNÓSTICO (JSON)
# OJO: si tu modal usa <form> clásico, esto debe pasar a Form(...)
# =========================================================
@router.post("/catalogo/test-diagnostico/preguntas")
async def crear_pregunta_diagnostico(
    request: Request,
    db: Session = Depends(get_db),
    usuario = Depends(get_current_user)
):
    # 🔐 Seguridad
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")

    form = await request.form()

    tipo = form.get("tipo_pregunta_codigo")
    area_id = form.get("area_id")
    dificultad = form.get("dificultad")
    enunciado = form.get("enunciado")
    opciones_json = form.get("opciones_json")
    respuesta_correcta = form.get("respuesta_correcta")

    # 🔎 Validaciones
    if not all([tipo, area_id, dificultad, enunciado, opciones_json, respuesta_correcta]):
        raise HTTPException(status_code=400, detail="Datos incompletos")

    if tipo != "SMUR":
        raise HTTPException(status_code=400, detail="Tipo de pregunta no soportado aún")

    try:
        opciones = json.loads(opciones_json)
    except Exception:
        raise HTTPException(status_code=400, detail="Opciones inválidas")

    if len(opciones) < 2:
        raise HTTPException(status_code=400, detail="Debe haber al menos 2 opciones")

    pregunta = PreguntaDiagnostico(
        area_id=int(area_id),              # 👈 coincide con tu modelo
        dificultad=dificultad,
        enunciado=enunciado,
        opciones=json.dumps(opciones),     # se guarda como TEXT
        respuesta_correcta=int(respuesta_correcta),
        activa=True,
        creado_por=usuario.id_usuario
    )

    db.add(pregunta)
    db.commit()

    # ✅ REDIRECCIÓN POST/REDIRECT/GET (correcto)
    return RedirectResponse(
        url="/admin/catalogo/test-diagnostico/preguntas",
        status_code=303
    )
