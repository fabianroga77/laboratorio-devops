from dataclasses import dataclass

from application.use_cases.clientes import ClienteUseCases
from application.use_cases.cuentas import CuentaUseCases
from application.use_cases.transacciones import TransaccionUseCases
from infrastructure.persistence.repositories.cliente_repo import MemoryClienteRepository
from infrastructure.persistence.repositories.cuenta_repo import MemoryCuentaRepository
from infrastructure.persistence.repositories.transaccion_repo import MemoryTransaccionRepository
from infrastructure.seed.seed_data import seed_if_empty


@dataclass
class AppContainer:
    cliente_uc: ClienteUseCases
    cuenta_uc: CuentaUseCases
    transaccion_uc: TransaccionUseCases


_container: AppContainer | None = None


def build_container() -> AppContainer:
    cliente_repo = MemoryClienteRepository()
    cuenta_repo = MemoryCuentaRepository()
    transaccion_repo = MemoryTransaccionRepository()

    seed_if_empty(cliente_repo, cuenta_repo, transaccion_repo)

    cuenta_uc = CuentaUseCases(cliente_repo, cuenta_repo)
    return AppContainer(
        cliente_uc=ClienteUseCases(cliente_repo),
        cuenta_uc=cuenta_uc,
        transaccion_uc=TransaccionUseCases(cuenta_uc, cuenta_repo, transaccion_repo),
    )


def get_container() -> AppContainer:
    global _container
    if _container is None:
        _container = build_container()
    return _container


def init_app() -> AppContainer:
    global _container
    _container = build_container()
    return _container
