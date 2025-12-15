from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# ===============================
# VISTA PRINCIPAL (RESULTADOS)
# ===============================
@router.get(
    "/test-socio-ocupacional",
    response_class=HTMLResponse,
    name="estudiante_test_socio"
)
async def test_socio_ocupacional(request: Request):
    return templates.TemplateResponse(
        "estudiante/test_socio_ocupacional.html",
        {"request": request}
    )


# ===============================
# VISTA DEL TEST (PREGUNTAS)
# ===============================
@router.get(
    "/test-socio-ocupacional/iniciar",
    response_class=HTMLResponse,
    name="estudiante_test_socio_iniciar"
)
async def iniciar_test_socio_ocupacional(request: Request):
    return templates.TemplateResponse(
        "estudiante/test_socio_ocupacional_test.html",
        {"request": request}
    )
