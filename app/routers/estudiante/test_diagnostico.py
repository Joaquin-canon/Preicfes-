from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routers.estudiante.router import router

templates = Jinja2Templates(directory="app/templates")

@router.get("/test_diagnostico", response_class=HTMLResponse, name="estudiante_test_diagnostico")
def test_diagnostico_view(request: Request):
    return templates.TemplateResponse(
        "estudiante/test_diagnostico.html",
        {"request": request}
    )
