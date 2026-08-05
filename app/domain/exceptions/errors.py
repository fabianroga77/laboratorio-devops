class DomainError(Exception):
    """Error base de reglas de negocio."""

    def __init__(self, message: str, code: str = "domain_error"):
        self.message = message
        self.code = code
        super().__init__(message)


class ClienteNotFoundError(DomainError):
    def __init__(self, cliente_id: str):
        super().__init__(f"Cliente '{cliente_id}' no existe", "cliente_not_found")


class CuentaNotFoundError(DomainError):
    def __init__(self, cuenta_id: str):
        super().__init__(f"Cuenta '{cuenta_id}' no existe", "cuenta_not_found")


class TransaccionNotFoundError(DomainError):
    def __init__(self, transaccion_id: str):
        super().__init__(
            f"Transaccion '{transaccion_id}' no existe", "transaccion_not_found"
        )


class SaldoInsuficienteError(DomainError):
    def __init__(self, cuenta_id: str):
        super().__init__(
            f"Saldo insuficiente en la cuenta '{cuenta_id}'", "saldo_insuficiente"
        )


class CuentaInactivaError(DomainError):
    def __init__(self, cuenta_id: str, estado: str):
        super().__init__(
            f"La cuenta '{cuenta_id}' esta {estado} y no permite movimientos",
            "cuenta_inactiva",
        )


class DocumentoDuplicadoError(DomainError):
    def __init__(self, documento: str):
        super().__init__(
            f"Ya existe un cliente con documento '{documento}'", "documento_duplicado"
        )


class IdempotencyConflictError(DomainError):
    def __init__(self, key: str):
        super().__init__(
            f"Ya existe una transaccion con la clave de idempotencia '{key}'",
            "idempotency_conflict",
        )
