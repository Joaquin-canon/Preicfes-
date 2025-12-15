from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routers.estudiante.router import router

templates = Jinja2Templates(directory="app/templates")

@router.get("/roadmap", response_class=HTMLResponse, name="estudiante_roadmap")
def roadmap(request: Request):
    return templates.TemplateResponse(
        "estudiante/roadmap.html",
        {"request": request}
    )
