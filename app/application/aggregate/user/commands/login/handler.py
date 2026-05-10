from datetime import datetime, timedelta
from logging import Logger
from uuid import uuid4

from app.domain.aggregate.auth import Session, SessionContainer
from app.domain.exceptions.invalid_credentials import InvalidCredentialsException
from app.domain.exceptions.user_not_found import UserNotFoundException
from app.domain.repositories.session_repository import SessionRepository
from app.domain.repositories.user_repository import UserRepository
from app.domain.services.encryption_service import EncryptionService

from .request import Request
from .response import Response

SESSION_TTL_DAYS = 1


class Handler:
    def __init__(
        self,
        user_repository: UserRepository,
        session_repository: SessionRepository,
        encryption_service: EncryptionService,
        logger: Logger,
    ) -> None:
        self.user_repository = user_repository
        self.session_repository = session_repository
        self.encryption_service = encryption_service
        self.logger = logger

    async def handle(self, request: Request, timestamp: datetime) -> Response:
        user = await self.user_repository.get_by_group_and_email(request.group, request.email)
        if user is None:
            raise UserNotFoundException("User not found")

        match, needs_rehash = self.encryption_service.verify(
            request.password, user.password_hash
        )
        if not match:
            raise InvalidCredentialsException()

        if needs_rehash:
            user.password_hash = self.encryption_service.hash(request.password)
            await self.user_repository.update(user)

        expiration_date = timestamp + timedelta(days=SESSION_TTL_DAYS)
        session = Session(
            id=uuid4(),
            user_id=user.id,
            token=str(uuid4()),
            expiration_date=expiration_date,
            created_at=timestamp,
            updated_at=timestamp,
        )
        await self.session_repository.create(session)

        session_container = SessionContainer.from_session_model(session, user)
        jwt = self.encryption_service.get_jwt(session_container)

        self.logger.info(f"User logged in: {user.id}")

        return Response(
            user_id=user.id,
            session_id=session.id,
            group=user.group,
            role=int(user.role),
            jwt=jwt,
            expiration_date=session.expiration_date,
        )
