from .base_domain_exception import BaseDomainException


class SessionIsnotValidException(BaseDomainException):
    def __init__(self, session_id: str):
        super().__init__(
            message=f"Session with ID {session_id} is not valid.",
            response_code=401
        )