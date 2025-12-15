from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get(
    "/home",
    response_class=HTMLResponse,
    name="estudiante_home"
)
async def home(request: Request):
    return templates.TemplateResponse(
        "estudiante/home.html",
        {"request": request}
    )