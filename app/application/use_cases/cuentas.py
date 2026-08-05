import uuid
from decimal import Decimal
from typing import List, Optional

from domain.enums import EstadoCuenta, TipoCuenta
from domain.exceptions import ClienteNotFoundError, CuentaNotFoundError
from domain.models.cuenta import Cuenta
from domain.ports.cliente_repository import ClienteRepository
from domain.ports.cuenta_repository import CuentaRepository


class CuentaUseCases:
    def __init__(
        self,
        cliente_repo: ClienteRepository,
        cuenta_repo: CuentaRepository,
    ):
        self._clientes = cliente_repo
        self._cuentas = cuenta_repo

    def abrir(
        self,
        cliente_id: str,
        tipo: TipoCuenta,
        saldo_inicial: Decimal = Decimal("0"),
    ) -> Cuenta:
        if not self._clientes.find_by_id(cliente_id):
            raise ClienteNotFoundError(cliente_id)
        if saldo_inicial < 0:
            raise ValueError("El saldo inicial no puede ser negativo")

        cuenta = Cuenta(
            id=str(uuid.uuid4()),
            numero_cuenta=self._cuentas.next_numero_cuenta(),
            cliente_id=cliente_id,
            tipo=tipo,
            saldo=saldo_inicial,
        )
        return self._cuentas.save(cuenta)

    def obtener(self, cuenta_id: str) -> Cuenta:
        cuenta = self._cuentas.find_by_id(cuenta_id)
        if not cuenta:
            raise CuentaNotFoundError(cuenta_id)
        return cuenta

    def listar(
        self,
        cliente_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> tuple[List[Cuenta], int]:
        return (
            self._cuentas.list_all(cliente_id, skip, limit),
            self._cuentas.count(cliente_id),
        )

    def cambiar_estado(self, cuenta_id: str, estado: EstadoCuenta) -> Cuenta:
        cuenta = self.obtener(cuenta_id)
        cuenta.cambiar_estado(estado)
        return self._cuentas.save(cuenta)
