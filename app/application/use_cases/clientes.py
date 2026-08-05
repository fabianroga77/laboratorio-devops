import uuid
from typing import List, Optional

from domain.exceptions import (
    ClienteNotFoundError,
    DocumentoDuplicadoError,
)
from domain.models.cliente import Cliente
from domain.ports.cliente_repository import ClienteRepository


class ClienteUseCases:
    def __init__(self, cliente_repo: ClienteRepository):
        self._clientes = cliente_repo

    def crear(self, nombre: str, documento: str, email: str) -> Cliente:
        if self._clientes.find_by_documento(documento):
            raise DocumentoDuplicadoError(documento)
        cliente = Cliente(
            id=str(uuid.uuid4()),
            nombre=nombre,
            documento=documento,
            email=email,
        )
        return self._clientes.save(cliente)

    def obtener(self, cliente_id: str) -> Cliente:
        cliente = self._clientes.find_by_id(cliente_id)
        if not cliente:
            raise ClienteNotFoundError(cliente_id)
        return cliente

    def listar(self, skip: int = 0, limit: int = 50) -> tuple[List[Cliente], int]:
        return self._clientes.list_all(skip, limit), self._clientes.count()

    def actualizar(
        self,
        cliente_id: str,
        nombre: Optional[str] = None,
        email: Optional[str] = None,
    ) -> Cliente:
        cliente = self.obtener(cliente_id)
        if nombre is not None:
            cliente.nombre = nombre
        if email is not None:
            cliente.email = email
        return self._clientes.save(cliente)

