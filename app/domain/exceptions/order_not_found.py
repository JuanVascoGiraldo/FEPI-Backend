from .base_domain_exception import BaseDomainException


class OrderNotFoundException(BaseDomainException):
    def __init__(self, order_id: str) -> None:
        super().__init__(
            message=f"Order with id '{order_id}' was not found.",
            response_code=404,
            name="order_not_found",
        )
