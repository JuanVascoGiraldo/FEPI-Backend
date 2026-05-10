from pydantic import BaseModel, Field
from uuid import UUID
from decimal import Decimal
from typing import List

from .order_item_status import OrderItemStatus


class OrderItem(BaseModel):
    id: UUID
    dish_id: UUID
    name: str
    unit_price: Decimal
    quantity: int = 1
    specifications: List[str] = Field(default_factory=list)
    status: OrderItemStatus = OrderItemStatus.PENDING

    def subtotal(self) -> Decimal:
        return self.unit_price * self.quantity
