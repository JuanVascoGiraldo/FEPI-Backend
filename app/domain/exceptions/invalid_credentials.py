from .base_domain_exception import BaseDomainException


class InvalidCredentialsException(BaseDomainException):
    def __init__(self) -> None:
        super().__init__(
            message="Invalid email or password.",
            response_code=401,
            name="invalid_credentials",
        )
