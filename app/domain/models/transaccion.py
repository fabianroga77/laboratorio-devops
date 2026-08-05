from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional

from domain.enums import TipoTransaccion


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Transaccion:
    id: str
    tipo: TipoTransaccion
    monto: Decimal
    cuenta_id: str
    cuenta_destino_id: Optional[str] = None
    referencia: str = ""
    descripcion: str = ""
    idempotency_key: Optional[str] = None
    created_at: datetime = field(default_factory=_utcnow)
