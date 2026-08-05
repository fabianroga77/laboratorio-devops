from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal

from domain.enums import EstadoCuenta, TipoCuenta
from domain.exceptions import CuentaInactivaError, SaldoInsuficienteError


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Cuenta:
    id: str
    numero_cuenta: str
    cliente_id: str
    tipo: TipoCuenta
    saldo: Decimal
    estado: EstadoCuenta = EstadoCuenta.ACTIVA
    created_at: datetime = field(default_factory=_utcnow)

    def _validar_operativa(self) -> None:
        if self.estado != EstadoCuenta.ACTIVA:
            raise CuentaInactivaError(self.id, self.estado.value)

    def consignar(self, monto: Decimal) -> None:
        self._validar_operativa()
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a cero")
        self.saldo += monto

    def retirar(self, monto: Decimal) -> None:
        self._validar_operativa()
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a cero")
        if self.saldo < monto:
            raise SaldoInsuficienteError(self.id)
        self.saldo -= monto

    def cambiar_estado(self, nuevo_estado: EstadoCuenta) -> None:
        if self.estado == EstadoCuenta.CERRADA:
            raise ValueError("No se puede modificar una cuenta cerrada")
        self.estado = nuevo_estado
