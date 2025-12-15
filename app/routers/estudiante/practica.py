from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get(
    "/practica",
    response_class=HTMLResponse,
    name="estudiante_practica"   # 👈 ESTO ES CLAVE
)
async def practica(request: Request):
    return templates.TemplateResponse(
        "estudiante/practica.html",
        {"request": request}
    )
