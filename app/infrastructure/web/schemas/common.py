from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    skip: int
    limit: int
    items: List[T]


class ErrorResponse(BaseModel):
    code: str
    message: str


class MontoCOP(BaseModel):
    """Montos en pesos colombianos, maximo 2 decimales."""

    monto: float = Field(..., gt=0, examples=[50000.0])
