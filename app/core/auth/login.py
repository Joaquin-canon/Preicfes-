from fastapi import APIRouter, Form, HTTPException, Depends, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.core.auth.jwt import create_access_token
from app.database.database import get_db
from app.models.usuario import Usuario

# ===============================
# ROUTER
# ===============================
router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# ===============================
# PASSWORD CONTEXT
# ===============================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ===============================
# NORMALIZAR PASSWORD
# ===============================
def normalize_password(password: str) -> str:
    return password.strip()[:72]  # bcrypt solo admite 72 bytes

# ===============================
# LOGIN ENDPOINT (API)
# ===============================
@router.post("/login")
def login(
    correo: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # ---------------------------
    # Normalizar correo
    # ---------------------------
    correo = correo.strip().lower()

    # ---------------------------
    # Buscar usuario
    # ---------------------------
    usuario = db.query(Usuario).filter(
        Usuario.correo == correo,
        Usuario.activo == True
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    # ---------------------------
    # Verificar password
    # ---------------------------
    password = normalize_password(password)

    if not pwd_context.verify(password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    # ---------------------------
    # Crear JWT
    # ---------------------------
    access_token = create_access_token(
        data={
            "sub": usuario.correo,
            "id_usuario": usuario.id_usuario,
            "rol": usuario.rol
        }
    )

    # ---------------------------
    # Respuesta API
    # ---------------------------
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "rol": usuario.rol
    }
