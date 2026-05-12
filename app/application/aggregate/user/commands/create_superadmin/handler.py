from datetime import datetime
from logging import Logger
from uuid import uuid4

from app.domain.aggregate.user import User
from app.domain.aggregate.user.email import Email
from app.domain.aggregate.user.user_role import UserRole
from app.domain.exceptions.email_already_exists import EmailAlreadyExistsException
from app.domain.repositories.user_repository import UserRepository
from app.domain.services.encryption_service import EncryptionService
from app.domain.services.email_service import EmailService

from .request import Request
from .response import Response


class Handler:
    def __init__(
        self,
        user_repository: UserRepository,
        encryption_service: EncryptionService,
        email_service: EmailService,
        logger: Logger,
    ) -> None:
        self.user_repository = user_repository
        self.encryption_service = encryption_service
        self.email_service = email_service
        self.logger = logger

    async def handle(self, request: Request, timestamp: datetime) -> Response:
        existing = await self.user_repository.get_by_group_and_email(None, request.email)
        if existing is not None:
            raise EmailAlreadyExistsException(request.email)

        user = User(
            id=uuid4(),
            group=None,
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

        try:
            await self.email_service.send_welcome(
                to=user.email,
                name=user.full_name(),
                role="Superadmin",
            )
        except Exception as exc:
            self.logger.error(f"Failed to send welcome email to {user.email.value}: {exc}")

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
