# app/routers/admin/catalogo.py

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import json

from app.core.templates import templates
from app.database.database import get_db
from app.core.auth.dependencies import get_current_user

from app.models.area import Area
from app.models.tipo_pregunta import TipoPregunta
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
        {"request": request, "config": config}
    )


# =========================================================
# TEST DIAGNÓSTICO - LISTAR PREGUNTAS
# =========================================================
@router.get("/catalogo/test-diagnostico/preguntas", response_class=HTMLResponse)
def listar_preguntas_diagnostico(
    request: Request,
    db: Session = Depends(get_db),
    usuario = Depends(get_current_user)   # 👈 DEPENDENCY BIEN USADA
):
    # 🔐 Validar rol
    if usuario.rol != "admin":
        return RedirectResponse("/login", status_code=302)

    preguntas = db.query(PreguntaDiagnostico).all()

    areas = (
        db.query(Area)
        .filter(Area.activa == True)
        .order_by(Area.nombre.asc())
        .all()
    )

    tipos_pregunta = (
        db.query(TipoPregunta)
        .filter(TipoPregunta.activa == True)
        .order_by(TipoPregunta.nombre.asc())
        .all()
    )

    return templates.TemplateResponse(
        "admin/formularios/test_diagnostico/banco_preguntas/preguntas.html",
        {
            "request": request,
            "preguntas": preguntas,
            "areas": areas,
            "tipos_pregunta": tipos_pregunta
        }
    )


# =========================================================
# CREAR PREGUNTA DIAGNÓSTICO (FORM HTML CLÁSICO)
# =========================================================
@router.post("/catalogo/test-diagnostico/preguntas")
async def crear_pregunta_diagnostico(
    request: Request,
    db: Session = Depends(get_db),
    usuario = Depends(get_current_user)
):
    # 🔐 Validar rol
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")

    # 📥 Leer formulario (CLAVE: await)
    form = await request.form()

    tipo = form.get("tipo_pregunta_codigo")
    area_id = form.get("area_id")
    dificultad = form.get("dificultad")
    enunciado = form.get("enunciado")
    opciones_json = form.get("opciones_json")
    respuesta_correcta = form.get("respuesta_correcta")

    # 🔎 Validación básica
    if not all([tipo, area_id, dificultad, enunciado, opciones_json, respuesta_correcta]):
        raise HTTPException(status_code=400, detail="Datos incompletos")

    # 🚫 Solo SMUR por ahora
   # ==============================
# VALIDACIÓN POR TIPO
# ==============================

    if tipo == "SMUR":
        if len(opciones) != 4:
            raise HTTPException(
                status_code=400,
                detail="SMUR debe tener exactamente 4 opciones"
            )

    elif tipo == "AFIRMACIONES":
        if len(opciones) != 2:
            raise HTTPException(
                status_code=400,
                detail="AFIRMACIONES debe tener exactamente 2 afirmaciones"
            )

    else:
        raise HTTPException(
            status_code=400,
            detail="Tipo de pregunta no soportado aún"
        )


    # 🔄 Opciones
    try:
        opciones = json.loads(opciones_json)
    except Exception:
        raise HTTPException(status_code=400, detail="Opciones inválidas")

    # ===============================
    # VALIDACIONES ICFES – SMUR
    # ===============================

    if len(enunciado.strip()) < 5:
        raise HTTPException(
            status_code=400,
            detail="El enunciado debe tener al menos 5 caracteres"
        )

    if not isinstance(opciones, list) or len(opciones) != 4:
        raise HTTPException(
            status_code=400,
            detail="Una pregunta SMUR debe tener exactamente 4 opciones"
        )

    opciones_limpias = [op.strip() for op in opciones]

    if any(not op for op in opciones_limpias):
        raise HTTPException(
            status_code=400,
            detail="Las opciones no pueden estar vacías"
        )

    if len(set(opciones_limpias)) != 4:
        raise HTTPException(
            status_code=400,
            detail="Las opciones no pueden repetirse"
        )

    try:
        respuesta_idx = int(respuesta_correcta)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="La respuesta correcta debe ser un índice válido"
        )

    if respuesta_idx < 0 or respuesta_idx >= 4:
        raise HTTPException(
            status_code=400,
            detail="La respuesta correcta no corresponde a una opción válida"
        )

    # ===============================

    tipo_pregunta = db.query(TipoPregunta).filter(
        TipoPregunta.codigo == tipo,
        TipoPregunta.activa == True
    ).first()

    if not tipo_pregunta:
        raise HTTPException(status_code=400, detail="Tipo de pregunta inválido")

    pregunta = PreguntaDiagnostico(
        area_id=int(area_id),
        tipo_pregunta_id=tipo_pregunta.id_tipo_pregunta,
        dificultad=dificultad,
        enunciado=enunciado.strip(),
        opciones=opciones_limpias,
        respuesta_correcta=respuesta_idx,
        activa=True,
        creado_por=usuario.id_usuario
    )

    db.add(pregunta)
    db.commit()

    return RedirectResponse(
        url="/admin/catalogo/test-diagnostico/preguntas",
        status_code=303
    )
@router.get(
    "/catalogo/test-diagnostico/tipos/{tipo}",
    response_class=HTMLResponse
)
def cargar_formulario_tipo(
    tipo: str,
    request: Request,
    usuario=Depends(get_current_user)
):
    if usuario.rol != "admin":
        raise HTTPException(status_code=403)

    tipos_validos = {
        "SMUR": "smur.html",
        "AFIRMACIONES": "afirmaciones.html",
        "CONTEXTO": "contexto.html",
        "IMAGEN": "imagen.html",
        "TABLA": "tabla.html",
    }

    archivo = tipos_validos.get(tipo.upper())
    if not archivo:
        raise HTTPException(status_code=404)

    return templates.TemplateResponse(
        f"admin/formularios/test_diagnostico/banco_preguntas/tipos/{archivo}",
        {"request": request}
    )