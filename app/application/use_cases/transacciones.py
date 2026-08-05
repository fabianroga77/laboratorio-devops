import uuid
from decimal import Decimal
from typing import List, Optional

from domain.enums import TipoTransaccion
from domain.exceptions import (
    CuentaNotFoundError,
    IdempotencyConflictError,
    TransaccionNotFoundError,
)
from domain.models.transaccion import Transaccion
from domain.ports.cuenta_repository import CuentaRepository
from domain.ports.transaccion_repository import TransaccionRepository
from application.use_cases.cuentas import CuentaUseCases


class TransaccionUseCases:
    def __init__(
        self,
        cuenta_use_cases: CuentaUseCases,
        cuenta_repo: CuentaRepository,
        transaccion_repo: TransaccionRepository,
    ):
        self._cuentas_uc = cuenta_use_cases
        self._cuentas = cuenta_repo
        self._transacciones = transaccion_repo

    def consignar(
        self,
        cuenta_id: str,
        monto: Decimal,
        referencia: str = "",
        descripcion: str = "",
    ) -> Transaccion:
        cuenta = self._cuentas_uc.obtener(cuenta_id)
        cuenta.consignar(monto)
        self._cuentas.save(cuenta)

        tx = Transaccion(
            id=str(uuid.uuid4()),
            tipo=TipoTransaccion.CONSIGNACION,
            monto=monto,
            cuenta_id=cuenta_id,
            referencia=referencia,
            descripcion=descripcion or "Consignacion",
        )
        return self._transacciones.save(tx)

    def retirar(
        self,
        cuenta_id: str,
        monto: Decimal,
        referencia: str = "",
        descripcion: str = "",
    ) -> Transaccion:
        cuenta = self._cuentas_uc.obtener(cuenta_id)
        cuenta.retirar(monto)
        self._cuentas.save(cuenta)

        tx = Transaccion(
            id=str(uuid.uuid4()),
            tipo=TipoTransaccion.RETIRO,
            monto=monto,
            cuenta_id=cuenta_id,
            referencia=referencia,
            descripcion=descripcion or "Retiro",
        )
        return self._transacciones.save(tx)

    def transferir(
        self,
        cuenta_origen_id: str,
        cuenta_destino_id: str,
        monto: Decimal,
        referencia: str = "",
        descripcion: str = "",
        idempotency_key: Optional[str] = None,
    ) -> Transaccion:
        if cuenta_origen_id == cuenta_destino_id:
            raise ValueError("No se puede transferir a la misma cuenta")

        if idempotency_key:
            existente = self._transacciones.find_by_idempotency_key(idempotency_key)
            if existente:
                raise IdempotencyConflictError(idempotency_key)

        origen = self._cuentas_uc.obtener(cuenta_origen_id)
        destino = self._cuentas.find_by_id(cuenta_destino_id)
        if not destino:
            raise CuentaNotFoundError(cuenta_destino_id)

        origen.retirar(monto)
        destino.consignar(monto)
        self._cuentas.save(origen)
        self._cuentas.save(destino)

        tx = Transaccion(
            id=str(uuid.uuid4()),
            tipo=TipoTransaccion.TRANSFERENCIA,
            monto=monto,
            cuenta_id=cuenta_origen_id,
            cuenta_destino_id=cuenta_destino_id,
            referencia=referencia,
            descripcion=descripcion or "Transferencia entre cuentas",
            idempotency_key=idempotency_key,
        )
        return self._transacciones.save(tx)

    def obtener(self, transaccion_id: str) -> Transaccion:
        tx = self._transacciones.find_by_id(transaccion_id)
        if not tx:
            raise TransaccionNotFoundError(transaccion_id)
        return tx

    def listar(
        self,
        cuenta_id: Optional[str] = None,
        tipo: Optional[TipoTransaccion] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> tuple[List[Transaccion], int]:
        return (
            self._transacciones.list_all(cuenta_id, tipo, skip, limit),
            self._transacciones.count(cuenta_id, tipo),
        )
