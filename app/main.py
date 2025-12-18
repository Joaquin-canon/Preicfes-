from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from app.core.auth.router import router as auth_router
from app.routers.login import router as login_router
from app.routers.estudiante.router import router as estudiante_router
from app.routers.admin.router import router as admin_router

app = FastAPI()

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Routers principales
app.include_router(login_router)
app.include_router(auth_router)
app.include_router(estudiante_router)
app.include_router(admin_router)

@app.get("/")
def root():
    return RedirectResponse(url="/login")
