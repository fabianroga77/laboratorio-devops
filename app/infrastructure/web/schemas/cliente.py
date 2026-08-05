from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ClienteCreateRequest(BaseModel):
    nombre: str = Field(..., min_length=2, examples=["Maria Gomez"])
    documento: str = Field(..., min_length=5, examples=["1030123456"])
    email: str = Field(..., examples=["maria@email.com"])


class ClienteUpdateRequest(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2)
    email: Optional[str] = None


class ClienteResponse(BaseModel):
    id: str
    nombre: str
    documento: str
    email: str
    activo: bool
    created_at: datetime

    model_config = {"from_attributes": True}
