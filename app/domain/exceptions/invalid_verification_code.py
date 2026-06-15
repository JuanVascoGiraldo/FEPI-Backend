from .base_domain_exception import BaseDomainException


class InvalidVerificationCodeException(BaseDomainException):
    def __init__(self) -> None:
        super().__init__(
            message="El enlace de recuperación es inválido.",
            response_code=400,
            name="invalid_verification_code",
        )
