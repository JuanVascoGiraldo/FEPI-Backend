from datetime import datetime, timezone
from logging import Logger
from uuid import uuid4

from app.domain.aggregate.user import User
from app.domain.aggregate.user.email import Email
from app.domain.aggregate.user.user_role import UserRole
from app.domain.exceptions.email_already_exists import EmailAlreadyExistsException
from app.domain.exceptions.group_not_found import GroupNotFoundException
from app.domain.repositories.user_repository import UserRepository
from app.domain.repositories.group_repository import GroupRepository
from app.domain.services.encryption_service import EncryptionService

from .request import Request, SUPERADMIN_GROUP
from .response import Response


class Handler:
    def __init__(
        self,
        user_repository: UserRepository,
        group_repository: GroupRepository,
        encryption_service: EncryptionService,
        logger: Logger,
    ) -> None:
        self.user_repository = user_repository
        self.group_repository = group_repository
        self.encryption_service = encryption_service
        self.logger = logger

    async def handle(self, request: Request, timestamp: datetime) -> Response:
        group = await self.group_repository.get_by_name(SUPERADMIN_GROUP)
        if group is None:
            raise GroupNotFoundException(SUPERADMIN_GROUP)

        existing = await self.user_repository.get_by_email(request.email)
        if existing is not None:
            raise EmailAlreadyExistsException(request.email)

        user = User(
            id=uuid4(),
            group=SUPERADMIN_GROUP,
            first_name=request.first_name,
            last_name=request.last_name,
            email=Email(value=request.email),
            password_hash=self.encryption_service.hash(request.password),
            role=UserRole.SUPERADMIN,
            is_active=True,
            phone=request.phone,
            created_at=timestamp,
            updated_at=timestamp,
        )

        await self.user_repository.create(user)
        self.logger.info(f"Superadmin created: {user.id}")

        return Response(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email.value,
            role=int(user.role),
            group=user.group,
            is_active=user.is_active,
            phone=user.phone,
            created_at=user.created_at,
        )
