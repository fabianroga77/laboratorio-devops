import platform
import time

from fastapi import APIRouter

from infrastructure.config import get_settings

router = APIRouter(tags=["Sistema"])

_start_time = time.time()


@router.get("/")
def root():
    """Info general del servicio."""
    settings = get_settings()
    return {
        "service": "core-banking-lite",
        "version": settings.app_version,
        "env": settings.app_env,
        "message": "Core bancario activo — ver /docs para la API",
    }


@router.get("/health")
def health_check():
    """Health check para los probes de Kubernetes."""
    return {"status": "ok", "env": get_settings().app_env}


@router.get("/info")
def info():
    """Datos del runtime del contenedor."""
    settings = get_settings()
    return {
        "service": "core-banking-lite",
        "version": settings.app_version,
        "env": settings.app_env,
        "python_version": platform.python_version(),
        "os": platform.system(),
        "storage": "memory",
        "uptime_seconds": round(time.time() - _start_time, 1),
    }
