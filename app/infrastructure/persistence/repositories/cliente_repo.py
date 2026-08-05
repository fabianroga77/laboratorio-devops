from typing import List, Optional

from domain.models.cliente import Cliente
from domain.ports.cliente_repository import ClienteRepository


class MemoryClienteRepository(ClienteRepository):
    def __init__(self) -> None:
        self._items: dict[str, Cliente] = {}

    def save(self, cliente: Cliente) -> Cliente:
        self._items[cliente.id] = cliente
        return cliente

    def find_by_id(self, cliente_id: str) -> Optional[Cliente]:
        return self._items.get(cliente_id)

    def find_by_documento(self, documento: str) -> Optional[Cliente]:
        for c in self._items.values():
            if c.documento == documento:
                return c
        return None

    def list_all(self, skip: int = 0, limit: int = 50) -> List[Cliente]:
        items = sorted(self._items.values(), key=lambda c: c.created_at)
        return items[skip : skip + limit]

    def count(self) -> int:
        return len(self._items)

    def bulk_insert(self, clientes: List[Cliente]) -> None:
        for c in clientes:
            self._items[c.id] = c
