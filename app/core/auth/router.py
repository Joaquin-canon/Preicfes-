from fastapi import APIRouter, Form, HTTPException, Depends, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import date

from app.database.database import get_db
from app.models.usuario import Usuario
from app.core.security import create_access_token

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

def hash_password(password: str) -> str:
    password = password.strip()[:72]
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_password = plain_password.strip()[:72]
    return pwd_context.verify(plain_password, hashed_password)

# ===============================
# REGISTER
# ===============================
@router.post("/register")
def register(
    nombres: str = Form(...),
    apellidos: str = Form(...),
    tipo_documento: str = Form(...),
    numero_documento: str = Form(...),
    correo: str = Form(...),
    password: str = Form(...),
    fecha_nacimiento: date = Form(...),
    rol: str = Form(...),
    db: Session = Depends(get_db)
):
    correo = correo.strip().lower()
    rol = rol.lower()

    if db.query(Usuario).filter(Usuario.correo == correo).first():
        raise HTTPException(status_code=400, detail="Correo ya registrado")

    if db.query(Usuario).filter(Usuario.numero_documento == numero_documento).first():
        raise HTTPException(status_code=400, detail="Documento ya registrado")

    usuario = Usuario(
        nombres=nombres,
        apellidos=apellidos,
        tipo_documento=tipo_documento,
        numero_documento=numero_documento,
        correo=correo,
        password_hash=hash_password(password),
        fecha_nacimiento=fecha_nacimiento,
        rol=rol,
        activo=True
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return {
        "message": "Usuario registrado correctamente",
        "id_usuario": usuario.id_usuario
    }

# ===============================
# LOGIN
# ===============================
@router.post("/login")
def login(
    correo: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    correo = correo.strip().lower()

    usuario = db.query(Usuario).filter(Usuario.correo == correo).first()

    if not usuario or not verify_password(password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    token_data = {
        "sub": usuario.correo,
        "id_usuario": usuario.id_usuario,
        "rol": usuario.rol
    }

    access_token = create_access_token(data=token_data)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "rol": usuario.rol
    }
