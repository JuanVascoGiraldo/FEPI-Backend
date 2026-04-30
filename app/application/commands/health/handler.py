from .request import Request
from .response import Response
from logging import Logger


class Handler():
    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    async def handle(self, _: Request) -> Response:
        return Response()
