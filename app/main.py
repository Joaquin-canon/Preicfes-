from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.routers.login import router as login_router
from app.core.auth.router import router as auth_router
from app.routers.estudiante.router import router as estudiante_router
from app.routers.admin.router import router as admin_router


def create_app() -> FastAPI:
    app = FastAPI()

    templates = Jinja2Templates(directory="app/templates")
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    app.include_router(login_router)
    app.include_router(auth_router)
    app.include_router(estudiante_router)
    app.include_router(admin_router)  # ← SOLO ESTE

    @app.get("/", response_class=HTMLResponse)
    async def root(request: Request):
        return templates.TemplateResponse("home/home.html", {"request": request})

    return app


app = create_app()
