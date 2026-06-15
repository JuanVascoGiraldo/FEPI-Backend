from .base_domain_exception import BaseDomainException


class VerificationExpiredException(BaseDomainException):
    def __init__(self) -> None:
        super().__init__(
            message="El enlace de recuperación ha expirado. Solicita uno nuevo.",
            response_code=400,
            name="verification_expired",
        )
