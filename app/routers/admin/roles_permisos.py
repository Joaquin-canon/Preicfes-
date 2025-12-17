from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/roles-permisos", tags=["Admin"])

templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse, name="admin_roles")
def roles_view(request: Request):
    return templates.TemplateResponse(
        "admin/roles.html",
        {"request": request}
    )

