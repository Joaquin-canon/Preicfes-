from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.usuario import Usuario

SECRET_KEY = "SUPER_SECRET_KEY_CAMBIAR"
ALGORITHM = "HS256"


def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> Usuario | RedirectResponse:

    token = request.cookies.get("access_token")

    if not token:
        return RedirectResponse("/login", status_code=302)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id_usuario")
    except JWTError:
        return RedirectResponse("/login", status_code=302)

    if not user_id:
        return RedirectResponse("/login", status_code=302)

    usuario = db.query(Usuario).filter(
        Usuario.id_usuario == user_id,
        Usuario.activo == True
    ).first()

    if not usuario:
        return RedirectResponse("/login", status_code=302)

    return usuario
