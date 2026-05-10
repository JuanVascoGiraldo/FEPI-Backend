from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID
from typing import List, Optional

from pydantic import EmailStr

from .base_dao import BaseDao


class PaymentDao(BaseDao):
    id: UUID
    amount: Decimal
    tip: Decimal
    email: EmailStr
    dish_ids: Optional[List[UUID]] = None
    created_at: datetime

    def build_pk(self) -> str:
        return ""

    def build_sk(self) -> str:
        return ""
