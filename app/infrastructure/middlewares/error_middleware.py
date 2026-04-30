from app.domain.exceptions.base_domain_exception import BaseDomainException
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Response, status, Request
from logging import getLogger
from orjson import dumps
from typing import Any
from pydantic import ValidationError


class ErrorMiddleWare(BaseHTTPMiddleware):

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Any:
        logger = getLogger(__name__)
        try:
            response = await call_next(request)
        except Exception as ex:
            logger.error("An exception has occured: %s ", ex, extra={
                "path": request.url.path,
                "method": request.method,
            })
            logger.exception(ex, exc_info=True, stack_info=True)
            if isinstance(ex, BaseDomainException):
                response = Response(
                    dumps({"name": ex.name, "message": ex.message}),
                    status_code=ex.response_code if ex.response_code else status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            elif isinstance(ex, ValidationError):
                errors = []
                for error in ex.errors():
                    field = ".".join(str(loc) for loc in error["loc"])
                    errors.append({
                        "field": field,
                        "message": error["msg"],
                        "type": error["type"]
                    })
                response = Response(
                    dumps({
                        "name": "validation_error",
                        "message": "Validation failed",
                        "errors": errors
                    }),
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            elif isinstance(ex, ValueError):
                raise ex
            else:
                response = Response(
                    dumps({"status": "An error has occurred"}),
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            response.headers["Content-Type"] = "application/json"
        logger.info("Request finished", extra={
            "path": request.url.path,
            "method": request.method,
            "status_code": response.status_code
        })
        return response
