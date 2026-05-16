from .base_domain_exception import BaseDomainException


class OrderItemNotFoundException(BaseDomainException):
    def __init__(self, item_id: str) -> None:
        super().__init__(
            message=f"Order item with id '{item_id}' was not found.",
            response_code=404,
            name="order_item_not_found",
        )
