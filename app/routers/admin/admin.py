from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.core.auth.roles import require_role

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(require_role("admin"))]
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    data = {
        "uptime": "99.98%",
        "errores": 3,
        "latencia": "120 ms",
        "estado": "Sistema estable"
    }

    return templates.TemplateResponse(
        "admin/dashboard.html",
        {
            "request": request,
            "data": data
        }
    )
