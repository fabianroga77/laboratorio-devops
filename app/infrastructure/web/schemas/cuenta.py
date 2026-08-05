from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from domain.enums import EstadoCuenta, TipoCuenta


class CuentaCreateRequest(BaseModel):
    cliente_id: str = Field(..., examples=["seed-cliente-001"])
    tipo: TipoCuenta = Field(..., examples=[TipoCuenta.AHORROS])
    saldo_inicial: float = Field(default=0, ge=0, examples=[100000.0])


class CuentaEstadoRequest(BaseModel):
    estado: EstadoCuenta = Field(..., examples=[EstadoCuenta.BLOQUEADA])


class CuentaResponse(BaseModel):
    id: str
    numero_cuenta: str
    cliente_id: str
    tipo: TipoCuenta
    saldo: float
    moneda: str = "COP"
    estado: EstadoCuenta
    created_at: datetime

    model_config = {"from_attributes": True}
