from fastapi import Depends, HTTPException, status
from app.core.auth.jwt import get_current_user
from app.models.usuario import Usuario

def require_role(*roles_permitidos: str):
    def role_checker(usuario: Usuario = Depends(get_current_user)):
        if usuario.rol not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para acceder a este recurso"
            )
        return usuario
    return role_checker
