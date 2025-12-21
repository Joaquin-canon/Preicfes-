from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.usuario import Usuario
from app.core.security import verify_password, create_access_token

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# ===============================
# GET LOGIN (VISTA)
# ===============================
@router.get("/login", response_class=HTMLResponse)
def login_view(request: Request):
    return templates.TemplateResponse(
        "login/login.html",
        {"request": request}
    )


# ===============================
# POST LOGIN (PROCESO REAL)
# ===============================
@router.post("/login")
def login_post(
    request: Request,
    correo: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    correo = correo.strip().lower()

    usuario = db.query(Usuario).filter(
        Usuario.correo == correo,
        Usuario.activo == True
    ).first()

    if not usuario or not verify_password(password, usuario.password_hash):
        return templates.TemplateResponse(
            "login/login.html",
            {
                "request": request,
                "error": "Credenciales incorrectas"
            },
            status_code=401
        )

    # ✅ Crear JWT
    access_token = create_access_token(
        data={
            "sub": usuario.correo,
            "id_usuario": usuario.id_usuario,
            "rol": usuario.rol
        }
    )

    # ✅ Redirección por rol
    destino = {
    "admin": "/admin/observabilidad",
    "docente": "/docente",
    "coordinador": "/coordinador",
    "estudiante": "/estudiante"
}.get(usuario.rol, "/login")

    # ✅ AQUÍ se crea la respuesta
    response = RedirectResponse(url=destino, status_code=302)

    # ✅ AQUÍ se guarda la cookie
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        samesite="lax",
        path="/"
    )

    # ✅ AQUÍ se retorna
    return response
