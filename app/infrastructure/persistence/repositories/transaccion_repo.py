from typing import List, Optional

from domain.enums import TipoTransaccion
from domain.models.transaccion import Transaccion
from domain.ports.transaccion_repository import TransaccionRepository


class MemoryTransaccionRepository(TransaccionRepository):
    def __init__(self) -> None:
        self._items: dict[str, Transaccion] = {}

    def save(self, transaccion: Transaccion) -> Transaccion:
        self._items[transaccion.id] = transaccion
        return transaccion

    def find_by_id(self, transaccion_id: str) -> Optional[Transaccion]:
        return self._items.get(transaccion_id)

    def find_by_idempotency_key(self, key: str) -> Optional[Transaccion]:
        for t in self._items.values():
            if t.idempotency_key == key:
                return t
        return None

    def list_all(
        self,
        cuenta_id: Optional[str] = None,
        tipo: Optional[TipoTransaccion] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Transaccion]:
        items = list(self._items.values())
        if cuenta_id:
            items = [
                t
                for t in items
                if t.cuenta_id == cuenta_id or t.cuenta_destino_id == cuenta_id
            ]
        if tipo:
            items = [t for t in items if t.tipo == tipo]
        items.sort(key=lambda t: t.created_at, reverse=True)
        return items[skip : skip + limit]

    def count(
        self,
        cuenta_id: Optional[str] = None,
        tipo: Optional[TipoTransaccion] = None,
    ) -> int:
        items = list(self._items.values())
        if cuenta_id:
            items = [
                t
                for t in items
                if t.cuenta_id == cuenta_id or t.cuenta_destino_id == cuenta_id
            ]
        if tipo:
            items = [t for t in items if t.tipo == tipo]
        return len(items)

    def bulk_insert(self, transacciones: List[Transaccion]) -> None:
        for t in transacciones:
            self._items[t.id] = t
