from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.core.templates import templates

router = APIRouter()

@router.get("/", response_class=HTMLResponse, name="admin_roles")
def roles_permisos(request: Request):
    return templates.TemplateResponse(
        "admin/roles/index.html",
        {"request": request}
    )
