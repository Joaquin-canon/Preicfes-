from fastapi import (
    APIRouter,
    Request,
    Depends,
    Form,
    HTTPException,
    UploadFile,
    File,
    Query,
)
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

import json
import os
import uuid

from app.core.templates import templates
from app.database.database import get_db

from app.models.area import Area
from app.models.tipo_pregunta import TipoPregunta

from app.models.pregunta_diagnostico import PreguntaDiagnostico
from fastapi import UploadFile, File, Form

# =========================================================
# ROUTER
# =========================================================
router = APIRouter(
    prefix="/catalogo",
    tags=["Admin - Catálogo"]
)

# =========================================================
# CATÁLOGO PRINCIPAL
# =========================================================
@router.get("", response_class=HTMLResponse)
def catalogo(request: Request):

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
            "descripcion": "Evaluación inicial"
        },
        {
            "nombre": "Test socio-ocupacional",
            "slug": "socio-ocupacional",
            "icono": "🧑‍💼",
            "descripcion": "Orientación vocacional"
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
# TEST → FORMULARIO
# =========================================================
@router.get("/tests/{slug}", response_class=HTMLResponse)
def gestionar_test(request: Request, slug: str):

    tests = {
        "test-diagnostico": {
            "slug": slug,
            "nombre": "Test diagnóstico breve"
        },
        "socio-ocupacional": {
            "slug": slug,
            "nombre": "Test socio-ocupacional"
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
# BANCO DE PREGUNTAS
# =========================================================
@router.get("/tests/{slug}/banco", response_class=HTMLResponse)
def banco_preguntas(
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
    # =========================
    # TESTS DISPONIBLES
    # =========================
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

    # =========================
    # QUERY BASE
    # =========================
    query = db.query(PreguntaDiagnostico)

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

    # =========================
    # PAGINACIÓN
    # =========================
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

    # =========================
    # DATOS PARA FILTROS
    # =========================
    areas = db.query(Area).filter(Area.activa == True).all()
    tipos_pregunta = db.query(TipoPregunta).filter(TipoPregunta.activa == True).all()

    # =========================
    # RENDER TEMPLATE (CLAVE)
    # =========================
    return templates.TemplateResponse(
        "admin/catalogo/preguntas/banco.html",
        {
            "request": request,
            "test": test,                     # 🔥 ESTO FALTABA
            "preguntas": preguntas,
            "areas": areas,
            "tipos_pregunta": tipos_pregunta,
            "page": page,
            "total_pages": total_pages,
            "filters": {                     # 🔥 ESTO FALTABA
                "area_id": area_id,
                "tipo_id": tipo_id,
                "dificultad": dificultad,
                "estado": estado,
                "q": q
            }
        }
    )



# =========================================================
# CREAR PREGUNTA
# =========================================================

@router.post("/tests/{slug}/preguntas")
async def crear_pregunta(
    slug: str,
    request: Request,
    area_id: int = Form(...),
    tipo_pregunta_codigo: str = Form(...),
    dificultad: str = Form(...),
    enunciado: str = Form(...),
    contexto: str = Form(None),
    opciones_json: str = Form(None),
    respuesta_correcta: str = Form(None),
    imagen: UploadFile = File(None),  
    db: Session = Depends(get_db)
):
    print("IMAGEN RECIBIDA:", imagen)

    tipo = db.query(TipoPregunta).filter(
        TipoPregunta.codigo == tipo_pregunta_codigo
    ).first()

    if not tipo:
        raise HTTPException(status_code=400, detail="Tipo inválido")

    opciones = json.loads(opciones_json)

    pregunta = PreguntaDiagnostico(
        area_id=area_id,
        tipo_pregunta_id=tipo.id_tipo_pregunta,
        dificultad=dificultad,
        contexto=contexto,
        enunciado=enunciado,
        opciones=opciones,
        respuesta_correcta=respuesta_correcta,
        activa=True,
    )

    # GUARDAR IMAGEN
    if imagen and imagen.filename:
        ext = imagen.filename.split(".")[-1]
        nombre = f"{uuid.uuid4()}.{ext}"

        carpeta = "app/static/uploads/preguntas"
        os.makedirs(carpeta, exist_ok=True)

        ruta = os.path.join(carpeta, nombre)
        contenido = await imagen.read()
        with open(ruta, "wb") as f:
            f.write(contenido)

        pregunta.imagen_url = f"/static/uploads/preguntas/{nombre}"

    db.add(pregunta)
    db.commit()

    return RedirectResponse(
        url=f"/admin/catalogo/tests/{slug}/banco",
        status_code=303
    )

# =========================================================
# EDITAR PREGUNTA (FORM)
# =========================================================
@router.get("/preguntas/{pregunta_id}/editar", response_class=HTMLResponse)
def editar_pregunta_form(
    request: Request,
    pregunta_id: int,
    db: Session = Depends(get_db),
):

    pregunta = db.query(PreguntaDiagnostico).get(pregunta_id)
    if not pregunta:
        raise HTTPException(status_code=404)

    areas = db.query(Area).filter(Area.activa == True).all()
    tipos_pregunta = db.query(TipoPregunta).filter(TipoPregunta.activa == True).all()

    return templates.TemplateResponse(
        "admin/catalogo/preguntas/edit.html",
        {
            "request": request,
            "pregunta": pregunta,
            "areas": areas,
            "tipos_pregunta": tipos_pregunta,
        }
    )

# =========================================================
# EDITAR PREGUNTA (GUARDAR)
# =========================================================
@router.post("/preguntas/{pregunta_id}/editar")
async def editar_pregunta_guardar(
    pregunta_id: int,
    db: Session = Depends(get_db),

    area_id: int = Form(...),
    dificultad: str = Form(...),
    contexto: str | None = Form(None),
    enunciado: str = Form(...),
    opciones_json: str = Form(...),
    respuesta_correcta: int | None = Form(None),
    imagen: UploadFile | None = File(None),
):

    pregunta = db.query(PreguntaDiagnostico).get(pregunta_id)
    if not pregunta:
        raise HTTPException(status_code=404)

    pregunta.area_id = area_id
    pregunta.dificultad = dificultad
    pregunta.contexto = contexto
    pregunta.enunciado = enunciado
    pregunta.opciones = json.loads(opciones_json)
    pregunta.respuesta_correcta = respuesta_correcta

    if imagen and imagen.filename:
        ext = imagen.filename.split(".")[-1]
        nombre = f"{uuid.uuid4()}.{ext}"

        carpeta = "app/static/uploads/preguntas"
        os.makedirs(carpeta, exist_ok=True)

        ruta = os.path.join(carpeta, nombre)
        with open(ruta, "wb") as f:
            f.write(imagen.file.read())

        pregunta.imagen_url = f"/static/uploads/preguntas/{nombre}"

    db.commit()

    return RedirectResponse(
        url="/admin/catalogo/tests/test-diagnostico/banco",
        status_code=303
    )

# ======================
# pre review 
# ========================
from app.models.pregunta_diagnostico import PreguntaDiagnostico

@router.get("/preguntas/{pregunta_id}/preview", response_class=HTMLResponse)
def preview_pregunta(
    pregunta_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    pregunta = db.query(PreguntaDiagnostico).get(pregunta_id)
    if not pregunta:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")

    return templates.TemplateResponse(
        "admin/catalogo/preguntas/preview.html",
        {
            "request": request,
            "pregunta": pregunta
        }
    )
