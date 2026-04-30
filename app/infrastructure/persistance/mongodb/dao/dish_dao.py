from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import ClassVar
from uuid import UUID

from .base_dao import BaseDao


DISH_PK_INDEX = "DISH#"
DISH_SK_INDEX = "INFO#"


class DishDao(BaseDao):
    PK: ClassVar[str] = DISH_PK_INDEX
    SK: ClassVar[str] = DISH_SK_INDEX

    id: UUID
    group: str
    name: str
    description: str
    price: Decimal
    category: int
    status_type: int
    status_description: str = ""
    image_url: str | None = None
    created_at: datetime
    updated_at: datetime

    def build_pk(self) -> str:
        return f"{self.PK}{self.id}"

    def build_sk(self) -> str:
        return self.SK
