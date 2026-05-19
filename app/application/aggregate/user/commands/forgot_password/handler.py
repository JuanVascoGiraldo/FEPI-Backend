import secrets
from datetime import datetime, timedelta, timezone
from logging import Logger
from uuid import uuid4

from app.config import Config
from app.domain.aggregate.auth import Verification, VerificationType
from app.domain.repositories.user_repository import UserRepository
from app.domain.repositories.verification_repository import VerificationRepository
from app.domain.services.email_service import EmailService

from .request import Request
from .response import Response

RESET_TTL_HOURS = 1


class Handler:
    def __init__(
        self,
        user_repository: UserRepository,
        verification_repository: VerificationRepository,
        email_service: EmailService,
        config: Config,
        logger: Logger,
    ) -> None:
        self.user_repository = user_repository
        self.verification_repository = verification_repository
        self.email_service = email_service
        self.config = config
        self.logger = logger

    async def handle(self, request: Request, timestamp: datetime) -> Response:
        user = await self.user_repository.get_by_group_and_email(request.group, request.email)

        # Always return 200 — never reveal whether the email exists
        if user is None:
            self.logger.info("Password reset requested for unknown email: %s", request.email)
            return Response(message="Si el correo existe, recibirás un enlace de recuperación.")

        # Invalidate any existing reset verification for this email
        existing = await self.verification_repository.get_by_value_and_type(
            str(request.email), VerificationType.PASSWORD_RESET
        )
        if existing is not None:
            await self.verification_repository.delete(existing.id)

        token = secrets.token_urlsafe(32)
        expiration = timestamp + timedelta(hours=RESET_TTL_HOURS)

        verification = Verification(
            id=uuid4(),
            value_id=str(request.email).lower(),
            type=VerificationType.PASSWORD_RESET,
            code=token,
            is_valid=False,
            created_at=timestamp,
            updated_at=timestamp,
            expiration_date=expiration,
        )
        await self.verification_repository.create(verification)

        reset_url = (
            f"{self.config.APP_URL}/reset-password"
            f"?token={token}&email={request.email}"
            + (f"&group={request.group}" if request.group else "")
        )

        try:
            await self.email_service.send_password_reset(
                to=user.email,
                name=user.full_name(),
                reset_url=reset_url,
            )
        except Exception as exc:
            self.logger.error("Failed to send password reset email to %s: %s", user.email, exc)

        self.logger.info("Password reset email sent to user: %s", user.id)
        return Response(message="Si el correo existe, recibirás un enlace de recuperación.")
