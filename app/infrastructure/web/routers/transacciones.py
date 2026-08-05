from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Header, Query

from domain.enums import TipoTransaccion
from infrastructure.web.dependencies import get_container
from infrastructure.web.mappers import to_transaccion_response
from infrastructure.web.schemas.common import PaginatedResponse
from infrastructure.web.schemas.transaccion import (
    ConsignacionRequest,
    RetiroRequest,
    TransferenciaRequest,
    TransaccionResponse,
)

router = APIRouter(prefix="/api/v1/transacciones", tags=["Transacciones"])


@router.post("/consignacion", response_model=TransaccionResponse, status_code=201)
def consignar(body: ConsignacionRequest):
    """Ingresa dinero a una cuenta."""
    tx = get_container().transaccion_uc.consignar(
        cuenta_id=body.cuenta_id,
        monto=Decimal(str(body.monto)),
        referencia=body.referencia,
        descripcion=body.descripcion,
    )
    return to_transaccion_response(tx)


@router.post("/retiro", response_model=TransaccionResponse, status_code=201)
def retirar(body: RetiroRequest):
    """Retira dinero de una cuenta. Falla si no hay saldo suficiente."""
    tx = get_container().transaccion_uc.retirar(
        cuenta_id=body.cuenta_id,
        monto=Decimal(str(body.monto)),
        referencia=body.referencia,
        descripcion=body.descripcion,
    )
    return to_transaccion_response(tx)


@router.post("/transferencia", response_model=TransaccionResponse, status_code=201)
def transferir(
    body: TransferenciaRequest,
    x_idempotency_key: Optional[str] = Header(None, alias="X-Idempotency-Key"),
):
    """
    Transfiere entre dos cuentas en una sola operacion.
    Header opcional X-Idempotency-Key evita duplicar la misma transferencia.
    """
    tx = get_container().transaccion_uc.transferir(
        cuenta_origen_id=body.cuenta_origen_id,
        cuenta_destino_id=body.cuenta_destino_id,
        monto=Decimal(str(body.monto)),
        referencia=body.referencia,
        descripcion=body.descripcion,
        idempotency_key=x_idempotency_key,
    )
    return to_transaccion_response(tx)


@router.get("", response_model=PaginatedResponse[TransaccionResponse])
def listar_transacciones(
    cuenta_id: Optional[str] = Query(None),
    tipo: Optional[TipoTransaccion] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    """Historial de movimientos. Filtra por cuenta y/o tipo."""
    items, total = get_container().transaccion_uc.listar(cuenta_id, tipo, skip, limit)
    return PaginatedResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=[to_transaccion_response(t) for t in items],
    )


@router.get("/{transaccion_id}", response_model=TransaccionResponse)
def obtener_transaccion(transaccion_id: str):
    """Detalle de una transaccion."""
    return to_transaccion_response(
        get_container().transaccion_uc.obtener(transaccion_id)
    )
