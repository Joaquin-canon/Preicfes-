from fastapi import Depends, Request, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.database.database import get_db
from app.models.usuario import Usuario

SECRET_KEY = "SUPER_SECRET_KEY_CAMBIAR"
ALGORITHM = "HS256"


def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> Usuario:
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id_usuario")
    except JWTError:
        raise HTTPException(status_code=401)

    if not user_id:
        raise HTTPException(status_code=401)

    usuario = db.query(Usuario).filter(
        Usuario.id_usuario == user_id,
        Usuario.activo == True
    ).first()

    if not usuario:
        raise HTTPException(status_code=401)

    return usuario
