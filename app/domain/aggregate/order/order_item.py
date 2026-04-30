from pydantic import BaseModel, Field
from uuid import UUID
from decimal import Decimal
from typing import List

from .order_item_status import OrderItemStatus


class OrderItem(BaseModel):
    id: UUID
    dish_id: UUID
    name: str         # snapshot so the order is self-contained even if menu changes
    unit_price: Decimal  # snapshot of price at order time
    quantity: int = 1
    specifications: List[str] = Field(default_factory=list)  # e.g. ["no onion", "extra spicy"]
    amount_paid: Decimal = Decimal("0")
    status: OrderItemStatus = OrderItemStatus.PENDING

    def subtotal(self) -> Decimal:
        return self.unit_price * self.quantity

    def pending(self) -> Decimal:
        return self.subtotal() - self.amount_paid

    def is_paid(self) -> bool:
        return self.amount_paid >= self.subtotal()

    def register_payment(self, amount: Decimal) -> None:
        """Applies a payment capped at the item subtotal."""
        self.amount_paid = min(self.amount_paid + amount, self.subtotal())
