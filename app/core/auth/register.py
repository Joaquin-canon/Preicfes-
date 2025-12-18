from fastapi import APIRouter, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import date

from app.database.database import get_db
from app.models.usuario import Usuario
from app.models.admin import Admin
from app.models.docente import Docente
from app.models.coordinador import Coordinador
from app.models.estudiante import Estudiante


# ===============================
# ROUTER
# ===============================
router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# ===============================
# PASSWORD HASH
# ===============================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    password = password.strip()   # elimina espacios raros
    password = password[:72]       # límite real de bcrypt
    return pwd_context.hash(password)


# ===============================
# REGISTER ENDPOINT
# ===============================
@router.post("/register")
def register(
    nombres: str = Form(...),
    apellidos: str = Form(...),
    tipo_documento: str = Form(...),          # CC, CE, TI
    numero_documento: str = Form(...),
    correo: str = Form(...).strip().lower(),
    password: str = Form(...),
    fecha_nacimiento: date = Form(...),       # YYYY-MM-DD
    rol: str = Form(...),                     # estudiante, docente, coordinador, admin
    db: Session = Depends(get_db)
):
    try:
        # ---------------------------
        # Normalización
        # ---------------------------
        tipo_documento = tipo_documento.upper()
        rol = rol.lower()

        # ---------------------------
        # Validaciones
        # ---------------------------
        if tipo_documento not in ["CC", "CE", "TI"]:
            raise HTTPException(
                status_code=400,
                detail="Tipo de documento no válido"
            )

        if rol not in ["estudiante", "docente", "coordinador", "admin"]:
            raise HTTPException(
                status_code=400,
                detail="Rol no reconocido"
            )

        if db.query(Usuario).filter(Usuario.correo == correo).first():
            raise HTTPException(
                status_code=400,
                detail="El correo ya está registrado"
            )

        if db.query(Usuario).filter(Usuario.numero_documento == numero_documento).first():
            raise HTTPException(
                status_code=400,
                detail="El documento ya está registrado"
            )
        if len(password.strip()) < 6:
            raise HTTPException(
                status_code=400,
                detail="La contraseña debe tener al menos 6 caracteres"
            )

        # ---------------------------
        # Crear usuario base
        # ---------------------------
        nuevo_usuario = Usuario(
            nombres=nombres,
            apellidos=apellidos,
            tipo_documento=tipo_documento,
            numero_documento=numero_documento,
            correo=correo.strip().lower(),
            password_hash=hash_password(password),
            fecha_nacimiento=fecha_nacimiento,
            rol=rol,
            activo=True
        )

        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)

        # ---------------------------
        # Crear registro según rol
        # ---------------------------
        if rol == "admin":
            db.add(Admin(id_usuario=nuevo_usuario.id_usuario))

        elif rol == "docente":
            db.add(Docente(id_usuario=nuevo_usuario.id_usuario))

        elif rol == "coordinador":
            db.add(Coordinador(id_usuario=nuevo_usuario.id_usuario))

        elif rol == "estudiante":
            db.add(
                Estudiante(
                    id_usuario=nuevo_usuario.id_usuario,
                    institucion="SIN DEFINIR"
                )
            )

        db.commit()

        # ---------------------------
        # Respuesta
        # ---------------------------
        return {
            "message": "Usuario registrado correctamente",
            "id_usuario": nuevo_usuario.id_usuario,
            "rol": rol
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al registrar usuario: {str(e)}"
        )
