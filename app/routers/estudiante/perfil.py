from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# ===============================
# PERFIL & AJUSTES
# ===============================
@router.get(
    "/perfil",
    response_class=HTMLResponse,
    name="estudiante_perfil"
)
async def perfil(request: Request):
    return templates.TemplateResponse(
        "estudiante/perfil.html",
        {"request": request}
    )


# ===============================
# EXPORTAR PROGRESO (PDF - futuro)
# ===============================
@router.get(
    "/perfil/exportar",
    response_class=HTMLResponse,
    name="estudiante_exportar_progreso"
)
async def exportar_progreso(request: Request):
    return templates.TemplateResponse(
        "estudiante/exportar_progreso.html",
        {"request": request}
    )
