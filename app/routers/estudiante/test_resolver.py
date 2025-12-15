from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routers.estudiante.router import router

templates = Jinja2Templates(directory="app/templates")

@router.get(
    "/test_resolver",
    response_class=HTMLResponse,
    name="estudiante_test_resolver"
)
def test_resolver(request: Request):
    return templates.TemplateResponse(
        "estudiante/test_resolver.html",
        {"request": request}
    )
