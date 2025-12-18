from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from app.core.auth.roles import require_role

from app.routers.admin.catalogo import router as catalogo_router
from .observabilidad import router as observabilidad_router
from .roles_permisos import router as roles_router
from .soporte import router as soporte_router

# Router principal ADMIN
router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(require_role("admin"))]  # ← SOLO valida
)

# Redirección al entrar a /admin
@router.get("/", include_in_schema=False)
def admin_root():
    return RedirectResponse(url="/admin/observabilidad")

# Sub-rutas admin
router.include_router(observabilidad_router, prefix="/observabilidad")
router.include_router(roles_router, prefix="/roles")
router.include_router(soporte_router, prefix="/soporte")
router.include_router(catalogo_router)  # /admin/catalogo-contenidos

