from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

# Routers
from app.routers.login import router as login_router
from app.core.auth.router import router as auth_router
from app.routers.estudiante.router import router as estudiante_router
from app.routers.admin.router import router as admin_router


def create_app() -> FastAPI:
    app = FastAPI()

    # Templates
    templates = Jinja2Templates(directory="app/templates")

    # Static files
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    # Routers
    app.include_router(login_router)
    app.include_router(auth_router)
    app.include_router(estudiante_router)
    app.include_router(admin_router)

    # HOME PÚBLICO (LANDING)
    @app.get("/", response_class=HTMLResponse)
    async def root(request: Request):
        return templates.TemplateResponse(
            "home/home.html",
            {"request": request}
        )

    return app


app = create_app()
