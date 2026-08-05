from enum import Enum


class TipoCuenta(str, Enum):
    AHORROS = "ahorros"
    CORRIENTE = "corriente"


class EstadoCuenta(str, Enum):
    ACTIVA = "activa"
    BLOQUEADA = "bloqueada"
    CERRADA = "cerrada"


class TipoTransaccion(str, Enum):
    CONSIGNACION = "consignacion"
    RETIRO = "retiro"
    TRANSFERENCIA = "transferencia"
