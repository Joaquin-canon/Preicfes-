from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix="/soporte",
    tags=["Soporte"]
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse, name="admin_soporte")
def soporte_view(request: Request):
    return templates.TemplateResponse(
        "admin/soporte.html",
        {"request": request}
    )
