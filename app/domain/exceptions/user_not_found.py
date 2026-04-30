from .base_domain_exception import BaseDomainException


class UserNotFoundException(BaseDomainException):
    def __init__(self, user_id: str) -> None:
        super().__init__(
            message=f"User with id '{user_id}' was not found.",
            response_code=404,
            name="user_not_found",
        )
