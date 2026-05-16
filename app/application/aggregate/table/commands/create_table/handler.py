from logging import Logger
from uuid import uuid4

from app.domain.aggregate.table import Table, TableStatus
from app.domain.aggregate.value_objects.meta import Meta
from app.domain.repositories.table_repository import TableRepository
from app.domain.exceptions import IsNotAuthorizedException
from app.domain.aggregate.user.user_role import UserRole

from .request import Request
from .response import Response


class Handler:
    def __init__(self, table_repository: TableRepository, logger: Logger) -> None:
        self.table_repository = table_repository
        self.logger = logger

    async def handle(self, request: Request, session: Meta) -> Response:
        if session.role != UserRole.ADMIN:
            raise IsNotAuthorizedException()

        timestamp = session.timestamp
        table = Table(
            id=uuid4(),
            group=session.group,
            number=request.number,
            description=request.description,
            status=TableStatus.ACTIVE,
            created_at=timestamp,
            updated_at=timestamp,
        )
        await self.table_repository.create(table)
        self.logger.info(f"Table created: {table.id} (#{table.number}) for group {table.group}")

        return Response(
            id=table.id,
            group=table.group,
            number=table.number,
            description=table.description,
            status=int(table.status),
            created_at=table.created_at,
            updated_at=table.updated_at,
        )
