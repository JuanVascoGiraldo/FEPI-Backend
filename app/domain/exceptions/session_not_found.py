from .base_domain_exception import BaseDomainException


class SessionNotFoundException(BaseDomainException):
    def __init__(self) -> None:
        super().__init__(
            message="Session not found or token is invalid.",
            response_code=401
        )
