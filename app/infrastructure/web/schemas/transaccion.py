from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from domain.enums import TipoTransaccion


class ConsignacionRequest(BaseModel):
    cuenta_id: str = Field(..., examples=["seed-cuenta-001"])
    monto: float = Field(..., gt=0, examples=[100000.0])
    referencia: str = Field(default="", examples=["REF-001"])
    descripcion: str = Field(default="", examples=["Consignacion en efectivo"])


class RetiroRequest(BaseModel):
    cuenta_id: str = Field(..., examples=["seed-cuenta-001"])
    monto: float = Field(..., gt=0, examples=[50000.0])
    referencia: str = Field(default="", examples=["REF-002"])
    descripcion: str = Field(default="", examples=["Retiro cajero"])


class TransferenciaRequest(BaseModel):
    cuenta_origen_id: str = Field(..., examples=["seed-cuenta-001"])
    cuenta_destino_id: str = Field(..., examples=["seed-cuenta-002"])
    monto: float = Field(..., gt=0, examples=[75000.0])
    referencia: str = Field(default="", examples=["TRF-001"])
    descripcion: str = Field(default="", examples=["Transferencia entre cuentas propias"])


class TransaccionResponse(BaseModel):
    id: str
    tipo: TipoTransaccion
    monto: float
    moneda: str = "COP"
    cuenta_id: str
    cuenta_destino_id: Optional[str] = None
    referencia: str
    descripcion: str
    created_at: datetime

    model_config = {"from_attributes": True}
