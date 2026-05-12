from __future__ import annotations

from datetime import datetime
from typing import ClassVar
from uuid import UUID

from pydantic import Field

from .base_dao import BaseDao
from .order_item_dao import OrderItemDao
from .payment_dao import PaymentDao


ORDER_PK_INDEX = "ORDER#"
ORDER_SK_INDEX = "INFO#"


class OrderDao(BaseDao):
    PK: ClassVar[str] = ORDER_PK_INDEX
    SK: ClassVar[str] = ORDER_SK_INDEX
    # group, table_id, waiter_id and status are excluded — they are used in MongoDB query filters.
    ENCRYPTED_FIELDS: ClassVar[frozenset[str]] = frozenset({"notes"})

    id: UUID
    group: str
    table_id: UUID
    waiter_id: UUID | None = None
    items: list[OrderItemDao] = Field(default_factory=list)
    payments: list[PaymentDao] = Field(default_factory=list)
    status: int
    notes: str | None = None
    created_at: datetime
    updated_at: datetime

    def build_pk(self) -> str:
        return f"{self.PK}{self.id}"

    def build_sk(self) -> str:
        return self.SK
