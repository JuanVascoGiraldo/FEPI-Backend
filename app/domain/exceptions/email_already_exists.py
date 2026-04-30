from .base_domain_exception import BaseDomainException


class EmailAlreadyExistsException(BaseDomainException):
    def __init__(self, email: str) -> None:
        super().__init__(
            message=f"The email '{email}' is already registered.",
            response_code=400,
            name="email_already_exists",
        )
