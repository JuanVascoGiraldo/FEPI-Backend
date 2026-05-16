from pydantic import BaseModel, Field
from uuid import UUID
from decimal import Decimal
from typing import List, Optional
from datetime import datetime

from .order_item import OrderItem
from .order_status import OrderStatus
from .order_item_status import OrderItemStatus
from .payment import Payment


class Order(BaseModel):
    id: UUID
    group: str
    table_id: UUID
    waiter_id: Optional[UUID] = None
    items: List[OrderItem] = Field(default_factory=list)
    payments: List[Payment] = Field(default_factory=list)
    status: OrderStatus = OrderStatus.OPEN
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    # ── item management ──────────────────────────────────────────────────────

    def get_item(self, item_id: UUID) -> Optional[OrderItem]:
        return next((i for i in self.items if i.id == item_id), None)

    def add_item(self, item: OrderItem, timestamp: datetime) -> None:
        self.items.append(item)
        self.updated_at = timestamp

    def remove_item(self, item_id: UUID, timestamp: datetime) -> None:
        self.items = [i for i in self.items if i.id != item_id]
        self.updated_at = timestamp

    def update_item_status(self, item_id: UUID, status: OrderItemStatus, timestamp: datetime) -> None:
        item = self.get_item(item_id)
        if item is not None:
            item.status = status
        self.updated_at = timestamp

    # ── payment management ───────────────────────────────────────────────────

    def add_payment(self, payment: Payment, timestamp: datetime) -> None:
        self.payments.append(payment)
        self.updated_at = timestamp

    # ── payment calculations ─────────────────────────────────────────────────

    def total(self) -> Decimal:
        return sum((i.subtotal() for i in self.items), Decimal("0"))

    def total_paid(self) -> Decimal:
        return sum((p.amount for p in self.payments if p.status == "confirmed"), Decimal("0"))

    def total_tips(self) -> Decimal:
        return sum((p.tip for p in self.payments), Decimal("0"))

    def total_pending(self) -> Decimal:
        return self.total() - self.total_paid()

    def is_fully_paid(self) -> bool:
        return self.total_pending() <= Decimal("0")

    # ── status transitions ───────────────────────────────────────────────────

    def start_process(self, timestamp: datetime) -> None:
        self.status = OrderStatus.IN_PROCESS
        self.updated_at = timestamp

    def mark_ready(self, timestamp: datetime) -> None:
        self.status = OrderStatus.READY
        self.updated_at = timestamp

    def start_payment(self, timestamp: datetime) -> None:
        self.status = OrderStatus.PAYING
        self.updated_at = timestamp

    def close(self, timestamp: datetime) -> None:
        self.status = OrderStatus.PAID
        self.updated_at = timestamp

    def cancel(self, timestamp: datetime) -> None:
        self.status = OrderStatus.CANCELLED
        self.updated_at = timestamp
