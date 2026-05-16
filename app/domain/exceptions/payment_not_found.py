from .base_domain_exception import BaseDomainException


class PaymentNotFoundException(BaseDomainException):
    def __init__(self, payment_id: str) -> None:
        super().__init__(f"Payment {payment_id} not found", response_code=404)
