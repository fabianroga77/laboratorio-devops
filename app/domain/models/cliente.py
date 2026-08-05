from dataclasses import dataclass, field
from datetime import datetime, timezone


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Cliente:
    id: str
    nombre: str
    documento: str
    email: str
    activo: bool = True
    created_at: datetime = field(default_factory=_utcnow)

    def desactivar(self) -> None:
        self.activo = False
