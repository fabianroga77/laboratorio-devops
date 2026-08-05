from domain.models.cliente import Cliente
from domain.models.cuenta import Cuenta
from domain.models.transaccion import Transaccion
from infrastructure.web.schemas.cliente import ClienteResponse
from infrastructure.web.schemas.cuenta import CuentaResponse
from infrastructure.web.schemas.transaccion import TransaccionResponse


def to_cliente_response(cliente: Cliente) -> ClienteResponse:
    return ClienteResponse(
        id=cliente.id,
        nombre=cliente.nombre,
        documento=cliente.documento,
        email=cliente.email,
        activo=cliente.activo,
        created_at=cliente.created_at,
    )


def to_cuenta_response(cuenta: Cuenta) -> CuentaResponse:
    return CuentaResponse(
        id=cuenta.id,
        numero_cuenta=cuenta.numero_cuenta,
        cliente_id=cuenta.cliente_id,
        tipo=cuenta.tipo,
        saldo=float(cuenta.saldo),
        estado=cuenta.estado,
        created_at=cuenta.created_at,
    )


def to_transaccion_response(tx: Transaccion) -> TransaccionResponse:
    return TransaccionResponse(
        id=tx.id,
        tipo=tx.tipo,
        monto=float(tx.monto),
        cuenta_id=tx.cuenta_id,
        cuenta_destino_id=tx.cuenta_destino_id,
        referencia=tx.referencia,
        descripcion=tx.descripcion,
        created_at=tx.created_at,
    )
