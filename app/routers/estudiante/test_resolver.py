from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get(
    "/test-resolver",
    response_class=HTMLResponse,
    name="estudiante_test_resolver"
)
async def test_resolver(request: Request):
    return templates.TemplateResponse(
        "estudiante/test_resolver.html",
        {"request": request}
    )