from .base_domain_exception import BaseDomainException


class VerificationNotFoundException(BaseDomainException):
    def __init__(self) -> None:
        super().__init__(
            message="Verification record not found.",
            response_code=404,
            name="verification_not_found",
        )
