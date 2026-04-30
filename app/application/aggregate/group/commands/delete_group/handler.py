from datetime import datetime, timezone
from logging import Logger
from uuid import UUID

from app.domain.exceptions.group_not_found import GroupNotFoundException
from app.domain.repositories.group_repository import GroupRepository

from .response import Response


class Handler:
    def __init__(self, group_repository: GroupRepository, logger: Logger) -> None:
        self.group_repository = group_repository
        self.logger = logger

    async def handle(self, group_id: UUID) -> Response:
        group = await self.group_repository.get_by_id(group_id)
        if group is None:
            raise GroupNotFoundException(str(group_id))

        group.is_active = False
        group.updated_at = datetime.now(timezone.utc)
        await self.group_repository.update(group)

        self.logger.info(f"Group deactivated: {group_id}")
        return Response()
