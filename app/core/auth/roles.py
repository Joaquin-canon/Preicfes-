from fastapi import Depends
from fastapi.responses import RedirectResponse
from app.core.auth.dependencies import get_current_user
from app.models.usuario import Usuario


def require_role(*roles: str):
    def checker(user=Depends(get_current_user)):
        # Si get_current_user devolvió RedirectResponse (no autenticado)
        if not isinstance(user, Usuario):
            return user  # redirección a /login

        # Si el usuario no tiene el rol requerido
        if user.rol not in roles:
            # puedes cambiar esta ruta por una página 403 propia
            return RedirectResponse("/login", status_code=302)

        return user

    return checker
