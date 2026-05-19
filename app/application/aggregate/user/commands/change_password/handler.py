from logging import Logger

from app.domain.aggregate.value_objects.meta import Meta
from app.domain.exceptions import InvalidCredentialsException, UserNotFoundException
from app.domain.repositories.user_repository import UserRepository
from app.domain.services.encryption_service import EncryptionService

from .request import Request
from .response import Response


class Handler:
    def __init__(
        self,
        user_repository: UserRepository,
        encryption_service: EncryptionService,
        logger: Logger,
    ) -> None:
        self.user_repository = user_repository
        self.encryption_service = encryption_service
        self.logger = logger

    async def handle(self, request: Request, session: Meta) -> Response:
        user = await self.user_repository.get_by_id(session.user_id)
        if user is None:
            raise UserNotFoundException("User not found")

        match, needs_rehash = self.encryption_service.verify(
            request.current_password, user.password_hash
        )
        if not match:
            raise InvalidCredentialsException()

        user.password_hash = self.encryption_service.hash(request.new_password)
        user.updated_at = session.timestamp
        await self.user_repository.update(user)

        self.logger.info("Password changed for user: %s", user.id)
        return Response(message="Password updated successfully")
