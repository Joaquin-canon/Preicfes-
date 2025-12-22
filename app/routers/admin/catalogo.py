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
# app/routers/admin/catalogo.py

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
    db: Session = Depends(get_db)
):
    # 🔐 Validación manual para HTML clásico
    try:
        usuario = get_current_user(request, db)
    except Exception:
        return RedirectResponse("/login", status_code=302)

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
# app/routers/admin/catalogo.py

# app/routers/admin/catalogo.py

@router.post("/catalogo/test-diagnostico/preguntas")
async def crear_pregunta_diagnostico(
    request: Request,
    db: Session = Depends(get_db),
    usuario = Depends(get_current_user)
):
    # 🔐 Validar rol
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")

    # 📥 Leer formulario
    form = await request.form()

    tipo = form.get("tipo_pregunta_codigo")
    area_id = form.get("area_id")
    dificultad = form.get("dificultad")
    enunciado = form.get("enunciado")
    opciones_json = form.get("opciones_json")
    respuesta_correcta = form.get("respuesta_correcta")

    # 🔎 Validaciones básicas
    if not all([tipo, area_id, dificultad, enunciado, opciones_json, respuesta_correcta]):
        raise HTTPException(status_code=400, detail="Datos incompletos")

    # 🚫 Por ahora solo SMUR
    if tipo != "SMUR":
        raise HTTPException(status_code=400, detail="Tipo de pregunta no soportado")

    # 🔄 Convertir opciones
    try:
        opciones = json.loads(opciones_json)
    except Exception:
        raise HTTPException(status_code=400, detail="Opciones inválidas")

    # =================================================
    # 🔒 VALIDACIONES ICFES – SMUR (AQUÍ VA)
    # =================================================

    # Enunciado mínimo
    if len(enunciado.strip()) < 5:
        raise HTTPException(
            status_code=400,
            detail="El enunciado debe tener al menos 10 caracteres"
        )

    # Exactamente 4 opciones
    if len(opciones) != 4:
        raise HTTPException(
            status_code=400,
            detail="Una pregunta SMUR debe tener exactamente 4 opciones"
        )

    # Opciones limpias y no vacías
    opciones_limpias = [op.strip() for op in opciones]

    if any(not op for op in opciones_limpias):
        raise HTTPException(
            status_code=400,
            detail="Las opciones no pueden estar vacías"
        )

    # Opciones no duplicadas
    if len(set(opciones_limpias)) != 4:
        raise HTTPException(
            status_code=400,
            detail="Las opciones no pueden repetirse"
        )

    # Respuesta correcta válida
    try:
        respuesta_idx = int(respuesta_correcta)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="La respuesta correcta debe ser un número"
        )

    if respuesta_idx < 0 or respuesta_idx >= 4:
        raise HTTPException(
            status_code=400,
            detail="La respuesta correcta no corresponde a una opción válida"
        )

    # =================================================

    # 🔍 Buscar tipo de pregunta en BD
    tipo_pregunta = db.query(TipoPregunta).filter(
        TipoPregunta.codigo == tipo,
        TipoPregunta.activa == True
    ).first()

    if not tipo_pregunta:
        raise HTTPException(status_code=400, detail="Tipo de pregunta inválido")

    # 🧩 Crear pregunta
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
