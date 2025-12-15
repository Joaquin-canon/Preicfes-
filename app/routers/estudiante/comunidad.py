from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# ===============================
# COMUNIDAD & AYUDA (VISTA PRINCIPAL)
# ===============================
@router.get(
    "/comunidad",
    response_class=HTMLResponse,
    name="estudiante_comunidad"
)
async def comunidad(request: Request):
    return templates.TemplateResponse(
        "estudiante/comunidad.html",
        {"request": request}
    )


# ===============================
# DETALLE DE PREGUNTA (FORO)
# ===============================
@router.get(
    "/comunidad/foro/{foro_id}",
    response_class=HTMLResponse,
    name="estudiante_foro_detalle"
)
async def foro_detalle(request: Request, foro_id: int):
    return templates.TemplateResponse(
        "estudiante/foro_detalle.html",
        {
            "request": request,
            "foro_id": foro_id
        }
    )


# ===============================
# PEDIR AYUDA
# ===============================
@router.get(
    "/comunidad/pedir-ayuda",
    response_class=HTMLResponse,
    name="estudiante_pedir_ayuda"
)
async def pedir_ayuda(request: Request):
    return templates.TemplateResponse(
        "estudiante/pedir_ayuda.html",
        {"request": request}
    )
