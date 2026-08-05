from fastapi import Request
from fastapi.responses import JSONResponse

from domain.exceptions import DomainError


def register_exception_handlers(app):
    @app.exception_handler(DomainError)
    async def domain_error_handler(_: Request, exc: DomainError):
        status = 400
        if exc.code.endswith("_not_found"):
            status = 404
        elif exc.code in ("documento_duplicado", "idempotency_conflict"):
            status = 409
        elif exc.code == "saldo_insuficiente":
            status = 422
        return JSONResponse(
            status_code=status,
            content={"code": exc.code, "message": exc.message},
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(_: Request, exc: ValueError):
        return JSONResponse(
            status_code=400,
            content={"code": "validation_error", "message": str(exc)},
        )
