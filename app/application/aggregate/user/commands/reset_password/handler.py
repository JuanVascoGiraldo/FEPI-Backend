from datetime import datetime
from logging import Logger

from app.domain.aggregate.auth import VerificationType
from app.domain.exceptions import (
    UserNotFoundException,
    VerificationNotFoundException,
    VerificationExpiredException,
    InvalidVerificationCodeException,
)
from app.domain.repositories.user_repository import UserRepository
from app.domain.repositories.verification_repository import VerificationRepository
from app.domain.services.encryption_service import EncryptionService

from .request import Request
from .response import Response


class Handler:
    def __init__(
        self,
        user_repository: UserRepository,
        verification_repository: VerificationRepository,
        encryption_service: EncryptionService,
        logger: Logger,
    ) -> None:
        self.user_repository = user_repository
        self.verification_repository = verification_repository
        self.encryption_service = encryption_service
        self.logger = logger

    async def handle(self, request: Request, timestamp: datetime) -> Response:
        verification = await self.verification_repository.get_by_value_and_type(
            str(request.email).lower(), VerificationType.PASSWORD_RESET
        )
        if verification is None:
            raise VerificationNotFoundException("No active password reset found for this email")

        if verification.is_expired(timestamp):
            await self.verification_repository.delete(verification.id)
            raise VerificationExpiredException("Password reset token has expired")

        if verification.code != request.token:
            raise InvalidVerificationCodeException("Invalid reset token")

        user = await self.user_repository.get_by_group_and_email(request.group, request.email)
        if user is None:
            raise UserNotFoundException("User not found")

        user.password_hash = self.encryption_service.hash(request.new_password)
        user.updated_at = timestamp
        await self.user_repository.update(user)

        await self.verification_repository.delete(verification.id)

        self.logger.info("Password reset completed for user: %s", user.id)
        return Response(message="Password reset successfully")
