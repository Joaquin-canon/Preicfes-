from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from app.core.auth.roles import require_role


from .home import router as home_router
from .dashboard import router as dashboard_router
from .practica import router as practica_router
from .preguntas import router as preguntas_router
from .roadmap import router as roadmap_router
from .test_diagnostico import router as test_diagnostico_router
from .test_resolver import router as test_resolver_router
from .test_socio_ocupacional import router as test_socio_router
from .comunidad import router as comunidad_router
from .perfil import router as perfil_router
from .faq import router as faq_router


router = APIRouter(
    prefix="/estudiante",
    tags=["Estudiante"],
    dependencies=[Depends(require_role("estudiante"))]  # 🔐 PROTECCIÓN GLOBAL
)

# 🔥 Redirect raíz
@router.get("/", include_in_schema=False)
async def estudiante_root():
    return RedirectResponse(url="/estudiante/home")

# Sub-rutas
router.include_router(home_router)
router.include_router(dashboard_router)
router.include_router(practica_router)
router.include_router(preguntas_router)
router.include_router(roadmap_router)
router.include_router(test_diagnostico_router)
router.include_router(test_resolver_router)
router.include_router(test_socio_router)
router.include_router(comunidad_router)
router.include_router(perfil_router)
router.include_router(faq_router)
