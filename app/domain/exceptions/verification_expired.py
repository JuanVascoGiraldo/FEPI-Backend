from .base_domain_exception import BaseDomainException


class VerificationExpiredException(BaseDomainException):
    def __init__(self) -> None:
        super().__init__(
            message="Verification code has expired. Please request a new one.",
            response_code=400,
            name="verification_expired",
        )
