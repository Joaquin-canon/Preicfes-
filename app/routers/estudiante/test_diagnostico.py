from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get(
    "/test-diagnostico",
    response_class=HTMLResponse,
    name="estudiante_test_diagnostico"
)
async def test_diagnostico(request: Request):
    return templates.TemplateResponse(
        "estudiante/test_diagnostico.html",
        {"request": request}
    )