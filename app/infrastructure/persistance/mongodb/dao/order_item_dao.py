from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from pydantic import ConfigDict, Field

from .base_dao import BaseDao


class OrderItemDao(BaseDao):
    model_config = ConfigDict(extra="ignore")

    id: UUID
    dish_id: UUID
    name: str
    unit_price: Decimal
    quantity: int
    specifications: list[str] = Field(default_factory=list)
    status: int

    def build_pk(self) -> str:
        return ""

    def build_sk(self) -> str:
        return ""
