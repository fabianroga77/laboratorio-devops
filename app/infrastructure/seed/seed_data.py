from decimal import Decimal

from domain.enums import TipoCuenta
from domain.models.cliente import Cliente
from domain.models.cuenta import Cuenta
from domain.ports.cliente_repository import ClienteRepository
from domain.ports.cuenta_repository import CuentaRepository
from domain.ports.transaccion_repository import TransaccionRepository


def seed_if_empty(
    cliente_repo: ClienteRepository,
    cuenta_repo: CuentaRepository,
    transaccion_repo: TransaccionRepository,
) -> None:
    """Datos de ejemplo al arrancar cada pod (memoria, no persiste entre deploys)."""
    if cliente_repo.count() > 0:
        return

    c1 = Cliente(
        id="seed-cliente-001",
        nombre="Ana Maria Lopez",
        documento="1010101010",
        email="ana.lopez@email.com",
    )
    c2 = Cliente(
        id="seed-cliente-002",
        nombre="Carlos Ruiz",
        documento="2020202020",
        email="carlos.ruiz@email.com",
    )
    if hasattr(cliente_repo, "bulk_insert"):
        cliente_repo.bulk_insert([c1, c2])
    else:
        cliente_repo.save(c1)
        cliente_repo.save(c2)

    cuentas = [
        Cuenta(
            id="seed-cuenta-001",
            numero_cuenta="ACC-2026-000001",
            cliente_id=c1.id,
            tipo=TipoCuenta.AHORROS,
            saldo=Decimal("1500000.00"),
        ),
        Cuenta(
            id="seed-cuenta-002",
            numero_cuenta="ACC-2026-000002",
            cliente_id=c1.id,
            tipo=TipoCuenta.CORRIENTE,
            saldo=Decimal("500000.00"),
        ),
        Cuenta(
            id="seed-cuenta-003",
            numero_cuenta="ACC-2026-000003",
            cliente_id=c2.id,
            tipo=TipoCuenta.AHORROS,
            saldo=Decimal("250000.00"),
        ),
    ]
    if hasattr(cuenta_repo, "bulk_insert"):
        cuenta_repo.bulk_insert(cuentas)
    else:
        for cuenta in cuentas:
            cuenta_repo.save(cuenta)

    if hasattr(transaccion_repo, "bulk_insert"):
        transaccion_repo.bulk_insert([])
