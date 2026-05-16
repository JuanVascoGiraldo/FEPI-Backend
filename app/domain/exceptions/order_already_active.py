from .base_domain_exception import BaseDomainException


class OrderAlreadyActiveException(BaseDomainException):
    def __init__(self, table_id: str) -> None:
        super().__init__(
            message=f"Table '{table_id}' already has an active order.",
            response_code=409,
            name="order_already_active",
        )
