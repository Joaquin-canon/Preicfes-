from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()  # SIN prefix

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse, name="admin_soporte")
def soporte(request: Request):
    return templates.TemplateResponse(
        "admin/soporte/index.html",
        {"request": request}
    )
