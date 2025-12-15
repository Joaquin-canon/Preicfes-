from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from app.routers.login import router as login_router
#estudiante 
import app.routers.estudiante  
from app.routers.estudiante.router import router as estudiante_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(login_router)
#estudiante
app.include_router(estudiante_router)

@app.get("/")
def root():
    return RedirectResponse(url="/login")
