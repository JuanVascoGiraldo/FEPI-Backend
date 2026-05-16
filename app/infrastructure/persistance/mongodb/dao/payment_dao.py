from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import ClassVar, List, Optional
from uuid import UUID

from pydantic import EmailStr

from .base_dao import BaseDao


class PaymentDao(BaseDao):
    # All payment fields are embedded inside OrderDao — none are used as top-level query filters.
    ENCRYPTED_FIELDS: ClassVar[frozenset[str]] = frozenset({
        "email", "amount", "tip", "name", "fiscal_info"
    })

    id: UUID
    amount: Decimal
    tip: Decimal
    email: EmailStr
    name: str = ""
    fiscal_info: Optional[str] = None
    payment_method: str = "cash"
    payment_type: str = "amount"
    status: str = "pending"
    dish_ids: Optional[List[UUID]] = None
    created_at: datetime

    def build_pk(self) -> str:
        return ""

    def build_sk(self) -> str:
        return ""
