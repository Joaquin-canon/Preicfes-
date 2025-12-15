from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get(
    "/dashboard",
    response_class=HTMLResponse,
    name="estudiante_dashboard"
)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        "estudiante/dashboard.html",
        {"request": request}
    )