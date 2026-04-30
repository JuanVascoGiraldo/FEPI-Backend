from .base_domain_exception import BaseDomainException


class DishNotAvailableException(BaseDomainException):
    def __init__(self, name: str, reason: str = "") -> None:
        detail = f" — {reason}" if reason else ""
        super().__init__(
            message=f"'{name}' is not available right now{detail}.",
            response_code=400,
            name="dish_not_available",
        )
