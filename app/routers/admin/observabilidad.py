from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.core.templates import templates

router = APIRouter()

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
