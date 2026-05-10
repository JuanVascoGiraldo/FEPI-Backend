from logging import Logger

from app.domain.repositories.user_repository import UserRepository
from app.domain.exceptions import IsNotAuthorizedException
from app.domain.aggregate.value_objects.meta import Meta
from app.domain.aggregate.user.user_role import UserRole

from .response import AdminItem, Response


class Handler:
    def __init__(self, user_repository: UserRepository, logger: Logger) -> None:
        self.user_repository = user_repository
        self.logger = logger

    async def handle(self, session: Meta) -> Response:
        if session.role != UserRole.SUPERADMIN:
            raise IsNotAuthorizedException()

        admins = await self.user_repository.get_by_role(UserRole.ADMIN)
        return Response(
            admins=[
                AdminItem(
                    id=u.id,
                    first_name=u.first_name,
                    last_name=u.last_name,
                    email=u.email.value,
                    group=u.group,
                    is_active=u.is_active,
                    phone=u.phone,
                    created_at=u.created_at,
                    updated_at=u.updated_at,
                )
                for u in admins
            ]
        )
