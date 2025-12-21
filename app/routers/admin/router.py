from fastapi import APIRouter

from app.routers.admin.observabilidad import router as observabilidad_router
from app.routers.admin.catalogo import router as catalogo_router
from app.routers.admin.roles_permisos import router as roles_router
from app.routers.admin.soporte import router as soporte_router

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

router.include_router(observabilidad_router)
router.include_router(catalogo_router)
router.include_router(roles_router)
router.include_router(soporte_router)
