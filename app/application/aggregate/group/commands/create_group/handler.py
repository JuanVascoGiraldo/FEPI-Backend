from logging import Logger
from uuid import uuid4

from app.domain.aggregate.group import Group
from app.domain.aggregate.value_objects.meta import Meta
from app.domain.repositories.group_repository import GroupRepository
from app.domain.exceptions import IsNotAuthorizedException
from app.domain.aggregate.user.user_role import UserRole

from .request import Request
from .response import Response


class Handler:
    def __init__(self, group_repository: GroupRepository, logger: Logger) -> None:
        self.group_repository = group_repository
        self.logger = logger

    async def handle(self, request: Request, session: Meta) -> Response:
        timestamp = session.timestamp
        if session.role != UserRole.SUPERADMIN:
            raise IsNotAuthorizedException()

        group = Group(
            id=uuid4(),
            name=request.name,
            is_active=True,
            created_at=timestamp,
            updated_at=timestamp,
        )
        await self.group_repository.create(group)
        self.logger.info(f"Group created: {group.id} ({group.name})")
        return Response(
            id=group.id,
            name=group.name,
            is_active=group.is_active,
            created_at=group.created_at,
            updated_at=group.updated_at,
        )
