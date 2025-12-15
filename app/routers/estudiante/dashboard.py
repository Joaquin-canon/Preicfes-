from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routers.estudiante.router import router

templates = Jinja2Templates(directory="app/templates")

@router.get(
    "/dashboard",
    response_class=HTMLResponse,
    name="estudiante_dashboard"
)
def dashboard(request: Request):
    return templates.TemplateResponse(
        "estudiante/dashboard.html",
        {"request": request}
    )
