from logging import Logger

from app.domain.repositories.group_repository import GroupRepository
from app.domain.exceptions import IsNotAuthorizedException
from app.domain.aggregate.value_objects.meta import Meta
from app.domain.aggregate.user.user_role import UserRole

from .response import GroupItem, Response


class Handler:
    def __init__(self, group_repository: GroupRepository, logger: Logger) -> None:
        self.group_repository = group_repository
        self.logger = logger

    async def handle(self, session: Meta) -> Response:
        if session.role != UserRole.SUPERADMIN:
            raise IsNotAuthorizedException()

        groups = await self.group_repository.get_all()
        return Response(
            groups=[
                GroupItem(
                    id=g.id,
                    name=g.name,
                    is_active=g.is_active,
                    created_at=g.created_at,
                    updated_at=g.updated_at,
                )
                for g in groups
            ]
        )
