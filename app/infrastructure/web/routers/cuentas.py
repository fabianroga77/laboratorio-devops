from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Query

from infrastructure.web.dependencies import get_container
from infrastructure.web.mappers import to_cuenta_response
from infrastructure.web.schemas.common import PaginatedResponse
from infrastructure.web.schemas.cuenta import (
    CuentaCreateRequest,
    CuentaEstadoRequest,
    CuentaResponse,
)

router = APIRouter(prefix="/api/v1/cuentas", tags=["Cuentas"])


@router.post("", response_model=CuentaResponse, status_code=201)
def abrir_cuenta(body: CuentaCreateRequest):
    """Abre una cuenta de ahorros o corriente para un cliente."""
    cuenta = get_container().cuenta_uc.abrir(
        cliente_id=body.cliente_id,
        tipo=body.tipo,
        saldo_inicial=Decimal(str(body.saldo_inicial)),
    )
    return to_cuenta_response(cuenta)


@router.get("", response_model=PaginatedResponse[CuentaResponse])
def listar_cuentas(
    cliente_id: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    """Lista cuentas. Se puede filtrar por cliente_id."""
    items, total = get_container().cuenta_uc.listar(cliente_id, skip, limit)
    return PaginatedResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=[to_cuenta_response(c) for c in items],
    )


@router.get("/{cuenta_id}", response_model=CuentaResponse)
def obtener_cuenta(cuenta_id: str):
    """Consulta una cuenta con su saldo actual."""
    return to_cuenta_response(get_container().cuenta_uc.obtener(cuenta_id))


@router.patch("/{cuenta_id}/estado", response_model=CuentaResponse)
def cambiar_estado_cuenta(cuenta_id: str, body: CuentaEstadoRequest):
    """Activa, bloquea o cierra una cuenta."""
    cuenta = get_container().cuenta_uc.cambiar_estado(cuenta_id, body.estado)
    return to_cuenta_response(cuenta)
