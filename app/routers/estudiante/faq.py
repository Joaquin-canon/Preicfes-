from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get(
    "/faq",
    response_class=HTMLResponse,
    name="estudiante_faq"
)
async def faq(request: Request):
    return templates.TemplateResponse(
        "estudiante/faq.html",
        {"request": request}
    )
