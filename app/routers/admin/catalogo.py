from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.core.templates import templates
from app.database.database import get_db
from fastapi import Query
from app.models.area import Area
from app.models.tipo_pregunta import TipoPregunta
from app.models.pregunta_diagnostico import PreguntaDiagnostico
from fastapi import Form
import json
from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import json

from app.database.database import get_db
from app.models.pregunta_diagnostico import PreguntaDiagnostico
from app.models.tipo_pregunta import TipoPregunta



router = APIRouter(
    prefix="/catalogo",
    tags=["Admin - Catálogo"]
)

# =========================================================
# CATÁLOGO PRINCIPAL
# =========================================================
@router.get("", response_class=HTMLResponse)
def catalogo(request: Request):

    """
    Vista principal del catálogo de áreas y tests especiales para el administrador.

    Se devuelve una respuesta HTML con una plantilla que contiene las áreas y tests especiales.

    Parameters:
    request (Request): solicitud HTTP.

    Returns:
    TemplateResponse: respuesta HTML con la plantilla renderizada.
    """
    areas = [
        {
            "codigo": "RM",
            "nombre": "Razonamiento matemático",
            "slug": "razonamiento-matematico",
            "icono": "📐",
            "descripcion": "Evaluación del pensamiento lógico y matemático."
        },
        {
            "codigo": "LC",
            "nombre": "Lectura crítica",
            "slug": "lectura-critica",
            "icono": "📘",
            "descripcion": "Comprensión, interpretación y análisis de textos."
        },
        {
            "codigo": "CN",
            "nombre": "Ciencias naturales",
            "slug": "ciencias-naturales",
            "icono": "🧪",
            "descripcion": "Análisis de fenómenos naturales desde el pensamiento científico."
        },
        {
            "codigo": "EN",
            "nombre": "Inglés",
            "slug": "ingles",
            "icono": "🇬🇧",
            "descripcion": "Comprensión lectora y uso del idioma inglés."
        },
        {
            "codigo": "CC",
            "nombre": "Competencias ciudadanas",
            "slug": "competencias-ciudadanas",
            "icono": "🌎",
            "descripcion": "Participación ciudadana, convivencia y pensamiento democrático."
        }
    ]

    tests_especiales = [
        {
            "nombre": "Test diagnóstico breve",
            "slug": "test-diagnostico",
            "icono": "🧠",
            "descripcion": "Evaluación inicial para determinar el nivel académico"
        },
        {
            "nombre": "Test socio-ocupacional",
            "slug": "socio-ocupacional",
            "icono": "🧑‍💼",
            "descripcion": "Orientación vocacional y ocupacional"
        }
    ]

    return templates.TemplateResponse(
        "admin/catalogo/catalogo.html",
        {
            "request": request,
            "areas": areas,
            "tests_especiales": tests_especiales
        }
    )

# =========================================================
# ÁREAS → MÓDULOS DE ESTUDIO
# =========================================================
@router.get("/areas/{slug}", response_class=HTMLResponse)
def gestionar_area(request: Request, slug: str):

    areas = {
        "razonamiento-matematico": {
            "codigo": "RM",
            "nombre": "Razonamiento matemático",
            "descripcion": "Evaluación del pensamiento lógico y matemático.",
            "estado": "Activo",
            "modulos_creados": 3,
            "modulos_activos": 3,
            "tiempo_total": "2h 30min"
        },
        "lectura-critica": {
            "codigo": "LC",
            "nombre": "Lectura crítica",
            "descripcion": "Comprensión, interpretación y análisis de textos.",
            "estado": "Activo",
            "modulos_creados": 2,
            "modulos_activos": 2,
            "tiempo_total": "1h 45min"
        },
        "ciencias-naturales": {
            "codigo": "CN",
            "nombre": "Ciencias naturales",
            "descripcion": "Pensamiento científico y análisis de fenómenos.",
            "estado": "Activo",
            "modulos_creados": 4,
            "modulos_activos": 3,
            "tiempo_total": "3h 10min"
        },
        "ingles": {
            "codigo": "EN",
            "nombre": "Inglés",
            "descripcion": "Comprensión lectora y uso del idioma inglés.",
            "estado": "Activo",
            "modulos_creados": 2,
            "modulos_activos": 2,
            "tiempo_total": "1h 20min"
        },
        "competencias-ciudadanas": {
            "codigo": "CC",
            "nombre": "Competencias ciudadanas",
            "descripcion": "Convivencia, participación y ciudadanía.",
            "estado": "Activo",
            "modulos_creados": 3,
            "modulos_activos": 3,
            "tiempo_total": "2h 00min"
        }
    }

    area = areas.get(slug)
    if not area:
        raise HTTPException(status_code=404, detail="Área no encontrada")

    return templates.TemplateResponse(
        "admin/catalogo/area_modulo.html",
        {
            "request": request,
            "area": area
        }
    )

# =========================================================
# TESTS → FORMULARIO PRINCIPAL
# =========================================================
@router.get("/tests/{slug}", response_class=HTMLResponse)
def gestionar_test(request: Request, slug: str):

    tests = {
        "test-diagnostico": {
            "slug": "test-diagnostico",
            "nombre": "Test diagnóstico breve",
            "descripcion": "Evaluación inicial para identificar el nivel académico del estudiante.",
            "estado": "Activo",
            "duracion": 20,
            "preguntas": 20,
            "intentos": 1,
            "uso": "Orientación académica"
        },
        "socio-ocupacional": {
            "slug": "socio-ocupacional",
            "nombre": "Test socio-ocupacional",
            "descripcion": "Evaluación de intereses, habilidades y orientación vocacional.",
            "estado": "Activo",
            "duracion": 25,
            "preguntas": 40,
            "intentos": 1,
            "uso": "Orientación vocacional"
        }
    }

    test = tests.get(slug)
    if not test:
        raise HTTPException(status_code=404, detail="Test no encontrado")

    return templates.TemplateResponse(
        "admin/catalogo/test_formulario.html",
        {
            "request": request,
            "test": test,
            "slug": slug
        }
    )

# =========================================================
# TESTS → BANCO DE PREGUNTAS (DESDE BD)
# =========================================================
@router.get("/tests/{slug}/banco", response_class=HTMLResponse)
def banco_preguntas_test(
    request: Request,
    slug: str,
    db: Session = Depends(get_db),

    page: int = Query(1, ge=1),
    area_id: str | None = Query(None),
    tipo_id: str | None = Query(None),
    dificultad: str | None = Query(None),
    estado: str | None = Query(None),
    q: str | None = Query(None),
):

    tests = {
        "test-diagnostico": {
            "slug": "test-diagnostico",
            "nombre": "Test diagnóstico breve",
            "descripcion": "Evaluación inicial"
        },
        "socio-ocupacional": {
            "slug": "socio-ocupacional",
            "nombre": "Test socio-ocupacional",
            "descripcion": "Orientación vocacional"
        }
    }

    test = tests.get(slug)
    if not test:
        raise HTTPException(status_code=404, detail="Test no encontrado")

    query = db.query(PreguntaDiagnostico)

    # ✅ CONVERSIÓN SEGURA
    if area_id:
        query = query.filter(PreguntaDiagnostico.area_id == int(area_id))

    if tipo_id:
        query = query.filter(PreguntaDiagnostico.tipo_pregunta_id == int(tipo_id))

    if dificultad:
        query = query.filter(PreguntaDiagnostico.dificultad == dificultad)

    if estado == "activa":
        query = query.filter(PreguntaDiagnostico.activa == True)

    if estado == "inactiva":
        query = query.filter(PreguntaDiagnostico.activa == False)

    if q:
        query = query.filter(PreguntaDiagnostico.enunciado.ilike(f"%{q}%"))

    # PAGINACIÓN
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

    areas = db.query(Area).filter(Area.activa == True).all()
    tipos_pregunta = db.query(TipoPregunta).filter(TipoPregunta.activa == True).all()

    return templates.TemplateResponse(
        "admin/catalogo/preguntas/banco.html",
        {
            "request": request,
            "test": test,
            "areas": areas,
            "tipos_pregunta": tipos_pregunta,
            "preguntas": preguntas,
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
from fastapi import Form
import json


@router.post("/tests/{slug}/preguntas")
def crear_pregunta_test(
    slug: str,
    db: Session = Depends(get_db),

    area_id: int = Form(...),
    tipo_pregunta_codigo: str = Form(...),
    dificultad: str = Form(...),

    contexto: str | None = Form(None),  # ✅ NUEVO
    enunciado: str = Form(...),

    opciones_json: str = Form(...),
    respuesta_correcta: int | None = Form(None),
):

    # 🔹 Validar test
    if slug not in ["test-diagnostico", "socio-ocupacional"]:
        raise HTTPException(status_code=404, detail="Test no válido")

    # 🔹 Buscar tipo de pregunta
    tipo = db.query(TipoPregunta).filter(
        TipoPregunta.codigo == tipo_pregunta_codigo
    ).first()

    if not tipo:
        raise HTTPException(status_code=400, detail="Tipo de pregunta inválido")

    # 🔹 Parsear opciones JSON
    try:
        opciones = json.loads(opciones_json)
    except Exception:
        raise HTTPException(status_code=400, detail="Opciones inválidas")

    # 🔹 Crear pregunta
    pregunta = PreguntaDiagnostico(
        area_id=area_id,
        tipo_pregunta_id=tipo.id_tipo_pregunta,
        dificultad=dificultad,
        enunciado=enunciado,
        opciones=opciones,
        respuesta_correcta=respuesta_correcta,
        activa=True,
    )

    db.add(pregunta)
    db.commit()

    # ✅ REDIRECCIÓN CORRECTA
    return RedirectResponse(
        url=f"/admin/catalogo/tests/{slug}/banco",
        status_code=303
    )

@router.post("/preguntas/{id}/toggle")
def toggle_pregunta(id: int, db: Session = Depends(get_db)):
    pregunta = db.query(PreguntaDiagnostico).get(id)

    if not pregunta:
        raise HTTPException(status_code=404)

    pregunta.activa = not pregunta.activa
    db.commit()

    return RedirectResponse(
        url="/admin/catalogo/tests/test-diagnostico/banco",
        status_code=303
    )
@router.get("/preguntas/{id}/preview", response_class=HTMLResponse)
def preview_pregunta(id: int, request: Request, db: Session = Depends(get_db)):
    pregunta = db.query(PreguntaDiagnostico).get(id)

    if not pregunta:
        raise HTTPException(status_code=404)

    return templates.TemplateResponse(
        "admin/catalogo/preguntas/preview.html",
        {
            "request": request,
            "pregunta": pregunta
        }
    )
    
    
@router.get("/tests/{slug}/preview", response_class=HTMLResponse)
def preview_test(request: Request, slug: str, db: Session = Depends(get_db)):
    preguntas = (
        db.query(PreguntaDiagnostico)
        .filter(PreguntaDiagnostico.activa == True)
        .limit(10)
        .all()
    )

    return templates.TemplateResponse(
        "admin/catalogo/tests/preview_test.html",
        {
            "request": request,
            "preguntas": preguntas
        }
    )   
    
# =========================================================
# EDITAR PREGUNTA (FORMULARIO)
# =========================================================
@router.get("/preguntas/{pregunta_id}/editar", response_class=HTMLResponse)
def editar_pregunta_form(
    request: Request,
    pregunta_id: int,
    db: Session = Depends(get_db),
):
    pregunta = (
        db.query(PreguntaDiagnostico)
        .filter(PreguntaDiagnostico.id_pregunta_diagnostico == pregunta_id)
        .first()
    )

    if not pregunta:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")

    areas = db.query(Area).filter(Area.activa == True).all()
    tipos_pregunta = db.query(TipoPregunta).filter(TipoPregunta.activa == True).all()

    return templates.TemplateResponse(
        "admin/catalogo/preguntas/edit.html",
        {
            "request": request,
            "pregunta": pregunta,
            "areas": areas,
            "tipos_pregunta": tipos_pregunta,
            "letras": ["A", "B", "C", "D", "E", "F"],  # ✔️
        }
    )
# =========================================================
# EDITAR PREGUNTA (GUARDAR)
# =========================================================
@router.post("/preguntas/{pregunta_id}/editar")
def editar_pregunta_guardar(
    pregunta_id: int,
    db: Session = Depends(get_db),

    area_id: int = Form(...),
    tipo_pregunta_codigo: str = Form(...),
    dificultad: str = Form(...),

    contexto: str | None = Form(None),      # ✅ NUEVO
    enunciado: str = Form(...),

    opciones_json: str = Form(...),
    respuesta_correcta: int | None = Form(None),

    imagen_url: str | None = Form(None),    # ✅ NUEVO
):
    pregunta = (
        db.query(PreguntaDiagnostico)
        .filter(PreguntaDiagnostico.id_pregunta_diagnostico == pregunta_id)
        .first()
    )

    if not pregunta:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")

    tipo = db.query(TipoPregunta).filter(
        TipoPregunta.codigo == tipo_pregunta_codigo
    ).first()

    if not tipo:
        raise HTTPException(status_code=400, detail="Tipo de pregunta inválido")

    try:
        opciones = json.loads(opciones_json)
    except Exception:
        raise HTTPException(status_code=400, detail="Opciones inválidas")

    # 🔹 ACTUALIZAR CAMPOS
    pregunta.area_id = area_id
    pregunta.tipo_pregunta_id = tipo.id_tipo_pregunta
    pregunta.dificultad = dificultad
    pregunta.contexto = contexto                # ✅
    pregunta.enunciado = enunciado
    pregunta.opciones = opciones
    pregunta.respuesta_correcta = respuesta_correcta
    pregunta.imagen_url = imagen_url             # ✅

    db.commit()

    return RedirectResponse(
        url="/admin/catalogo/tests/test-diagnostico/banco",
        status_code=303
    )
