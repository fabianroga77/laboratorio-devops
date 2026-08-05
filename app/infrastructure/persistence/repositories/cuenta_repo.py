from datetime import datetime, timezone
from typing import List, Optional

from domain.models.cuenta import Cuenta
from domain.ports.cuenta_repository import CuentaRepository


class MemoryCuentaRepository(CuentaRepository):
    def __init__(self) -> None:
        self._items: dict[str, Cuenta] = {}

    def save(self, cuenta: Cuenta) -> Cuenta:
        self._items[cuenta.id] = cuenta
        return cuenta

    def find_by_id(self, cuenta_id: str) -> Optional[Cuenta]:
        return self._items.get(cuenta_id)

    def find_by_numero(self, numero_cuenta: str) -> Optional[Cuenta]:
        for c in self._items.values():
            if c.numero_cuenta == numero_cuenta:
                return c
        return None

    def list_all(
        self, cliente_id: Optional[str] = None, skip: int = 0, limit: int = 50
    ) -> List[Cuenta]:
        items = list(self._items.values())
        if cliente_id:
            items = [c for c in items if c.cliente_id == cliente_id]
        items.sort(key=lambda c: c.created_at)
        return items[skip : skip + limit]

    def count(self, cliente_id: Optional[str] = None) -> int:
        if not cliente_id:
            return len(self._items)
        return sum(1 for c in self._items.values() if c.cliente_id == cliente_id)

    def next_numero_cuenta(self) -> str:
        year = datetime.now(timezone.utc).year
        prefix = f"ACC-{year}-"
        numeros = [
            int(c.numero_cuenta.split("-")[-1])
            for c in self._items.values()
            if c.numero_cuenta.startswith(prefix)
        ]
        siguiente = max(numeros, default=0) + 1
        return f"{prefix}{siguiente:06d}"

    def bulk_insert(self, cuentas: List[Cuenta]) -> None:
        for c in cuentas:
            self._items[c.id] = c
