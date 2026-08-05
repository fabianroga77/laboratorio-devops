from abc import ABC, abstractmethod
from typing import List, Optional

from domain.models.cuenta import Cuenta


class CuentaRepository(ABC):
    @abstractmethod
    def save(self, cuenta: Cuenta) -> Cuenta:
        pass

    @abstractmethod
    def find_by_id(self, cuenta_id: str) -> Optional[Cuenta]:
        pass

    @abstractmethod
    def find_by_numero(self, numero_cuenta: str) -> Optional[Cuenta]:
        pass

    @abstractmethod
    def list_all(
        self, cliente_id: Optional[str] = None, skip: int = 0, limit: int = 50
    ) -> List[Cuenta]:
        pass

    @abstractmethod
    def count(self, cliente_id: Optional[str] = None) -> int:
        pass

    @abstractmethod
    def next_numero_cuenta(self) -> str:
        pass
