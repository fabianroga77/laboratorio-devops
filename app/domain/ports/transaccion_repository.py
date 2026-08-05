from abc import ABC, abstractmethod
from typing import List, Optional

from domain.enums import TipoTransaccion
from domain.models.transaccion import Transaccion


class TransaccionRepository(ABC):
    @abstractmethod
    def save(self, transaccion: Transaccion) -> Transaccion:
        pass

    @abstractmethod
    def find_by_id(self, transaccion_id: str) -> Optional[Transaccion]:
        pass

    @abstractmethod
    def find_by_idempotency_key(self, key: str) -> Optional[Transaccion]:
        pass

    @abstractmethod
    def list_all(
        self,
        cuenta_id: Optional[str] = None,
        tipo: Optional[TipoTransaccion] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Transaccion]:
        pass

    @abstractmethod
    def count(
        self,
        cuenta_id: Optional[str] = None,
        tipo: Optional[TipoTransaccion] = None,
    ) -> int:
        pass
