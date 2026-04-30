from datetime import datetime, timedelta
from logging import Logger
from uuid import uuid4

from app.domain.aggregate.auth import SessionContainer
from app.domain.exceptions import (
    SessionIsnotValidException,  UserNotFoundException)
from app.domain.repositories.session_repository import SessionRepository
from app.domain.repositories.user_repository import UserRepository
from app.domain.services.encryption_service import EncryptionService
from uuid import UUID
from .request import Request
from app.domain.aggregate.value_objects.meta import Meta as Response

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
        self.logger.info(f"Validating session: {request.token}")
        payload = self.encryption_service.decode_jwt(request.token)
        user = await self.user_repository.get_by_id(UUID(payload.user_id))
        if user is None:
            raise UserNotFoundException(payload.user_id)

        session = await self.session_repository.get_by_id(UUID(payload.session_id))
        if session is None:
            raise SessionIsnotValidException(payload.session_id)
        
        if not session.is_active(timestamp):
            raise SessionIsnotValidException(payload.session_id)

        session_container = SessionContainer(
            id=str(session.id),
            user_id=str(user.id),
            session_id=str(session.id),
            expire_at=session.expiration_date.isoformat(),
            created_at=session.created_at.isoformat(),
            updated_at=session.updated_at.isoformat(),
            token=session.token,
            role=user.role.value,
        )
        if session_container != payload:
            self.logger.info("Session payload doesn't match")
            raise SessionIsnotValidException(payload.session_id)

        return Response(
            user_id=user.id,
            session_id=session.id,
            group=user.group,
            role=user.role,
            jwt=request.token,
            timestamp=timestamp,
        )
