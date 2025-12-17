from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse, name="admin_observabilidad")
def panel_observabilidad(request: Request):
    data = {
        "uptime": "99.98%",
        "errores": 3,
        "latencia": "120 ms",
        "estado": "Sistema estable"
    }

    return templates.TemplateResponse(
        "admin/observabilidad.html",
        {
            "request": request,
            "data": data
        }
    )
