from .base_domain_exception import BaseDomainException


class SessionExpiredException(BaseDomainException):
    def __init__(self) -> None:
        super().__init__(
            message="Session has expired. Please log in again.",
            response_code=401
        )
