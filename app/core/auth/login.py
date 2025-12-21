from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database.database import get_db
from app.models.usuario import Usuario
from app.core.auth.jwt import create_access_token

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(tags=["Login"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def normalize_password(password: str) -> str:
    return password.strip()[:72]


# -----------------------------
# MOSTRAR FORMULARIO
# -----------------------------
@router.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )


# -----------------------------
# PROCESAR LOGIN
# -----------------------------
@router.post("/login")
def login_submit(
    request: Request,
    correo: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    correo = correo.strip().lower()
    password = normalize_password(password)

    usuario = db.query(Usuario).filter(
        Usuario.correo == correo,
        Usuario.activo == True
    ).first()

    if not usuario or not pwd_context.verify(password, usuario.password_hash):
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Correo o contraseña incorrectos"
            },
            status_code=401
        )

    # Crear JWT
    token = create_access_token(
        data={
            "id_usuario": usuario.id_usuario,
            "rol": usuario.rol
        }
    )

    # Redirección por rol
    if usuario.rol == "admin":
        response = RedirectResponse("/admin", status_code=302)
    elif usuario.rol == "docente":
        response = RedirectResponse("/docente", status_code=302)
    elif usuario.rol == "coordinador":
        response = RedirectResponse("/coordinador", status_code=302)
    else:
        response = RedirectResponse("/estudiante", status_code=302)

    # Cookie HttpOnly
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False  # pon True en producción con HTTPS
    )

    return response
