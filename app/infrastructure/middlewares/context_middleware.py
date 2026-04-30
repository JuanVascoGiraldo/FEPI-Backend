from typing import Any
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request


class ContextMiddleware(BaseHTTPMiddleware):

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Any:
        try:
            response = await call_next(request)
        except Exception as ex:
            raise ex
        return response
