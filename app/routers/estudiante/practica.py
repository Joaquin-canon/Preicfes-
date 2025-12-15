from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routers.estudiante.router import router

templates = Jinja2Templates(directory="app/templates")


@router.get(
    "/practica",
    response_class=HTMLResponse,
    name="estudiante_practica"
)
def practica_view(request: Request):
    return templates.TemplateResponse(
        "estudiante/practica.html",
        {
            "request": request
        }
    )
