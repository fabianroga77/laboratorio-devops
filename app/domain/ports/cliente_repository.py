from abc import ABC, abstractmethod
from typing import List, Optional

from domain.models.cliente import Cliente


class ClienteRepository(ABC):
    @abstractmethod
    def save(self, cliente: Cliente) -> Cliente:
        pass

    @abstractmethod
    def find_by_id(self, cliente_id: str) -> Optional[Cliente]:
        pass

    @abstractmethod
    def find_by_documento(self, documento: str) -> Optional[Cliente]:
        pass

    @abstractmethod
    def list_all(self, skip: int = 0, limit: int = 50) -> List[Cliente]:
        pass

    @abstractmethod
    def count(self) -> int:
        pass
