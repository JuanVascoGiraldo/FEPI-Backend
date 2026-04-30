from .base_domain_exception import BaseDomainException


class InvalidVerificationCodeException(BaseDomainException):
    def __init__(self) -> None:
        super().__init__(
            message="The verification code provided is incorrect.",
            response_code=400,
            name="invalid_verification_code",
        )
