from typing import Optional

from fastapi import APIRouter, Query

from infrastructure.web.dependencies import get_container
from infrastructure.web.mappers import to_cliente_response
from infrastructure.web.schemas.cliente import (
    ClienteCreateRequest,
    ClienteResponse,
    ClienteUpdateRequest,
)
from infrastructure.web.schemas.common import PaginatedResponse

router = APIRouter(prefix="/api/v1/clientes", tags=["Clientes"])


@router.post("", response_model=ClienteResponse, status_code=201)
def crear_cliente(body: ClienteCreateRequest):
    """Registra un cliente nuevo en el banco."""
    cliente = get_container().cliente_uc.crear(
        nombre=body.nombre,
        documento=body.documento,
        email=body.email,
    )
    return to_cliente_response(cliente)


@router.get("", response_model=PaginatedResponse[ClienteResponse])
def listar_clientes(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    """Lista clientes con paginacion simple."""
    items, total = get_container().cliente_uc.listar(skip, limit)
    return PaginatedResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=[to_cliente_response(c) for c in items],
    )


@router.get("/{cliente_id}", response_model=ClienteResponse)
def obtener_cliente(cliente_id: str):
    """Detalle de un cliente por ID."""
    return to_cliente_response(get_container().cliente_uc.obtener(cliente_id))


@router.patch("/{cliente_id}", response_model=ClienteResponse)
def actualizar_cliente(cliente_id: str, body: ClienteUpdateRequest):
    """Actualiza nombre o email de un cliente."""
    cliente = get_container().cliente_uc.actualizar(
        cliente_id,
        nombre=body.nombre,
        email=body.email,
    )
    return to_cliente_response(cliente)
