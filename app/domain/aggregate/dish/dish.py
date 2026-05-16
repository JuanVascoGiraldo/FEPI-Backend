from pydantic import BaseModel, computed_field
from uuid import UUID
from decimal import Decimal
from typing import Optional
from datetime import datetime, timezone

from .food_category import FoodCategory
from .dish_status import DishStatus
from .dish_status_type import DishStatusType

TAX_RATE = Decimal("0.16")


class Dish(BaseModel):
    id: UUID
    group: str  # restaurant identifier this dish belongs to
    name: str
    description: str
    price: Decimal
    category: FoodCategory
    status: DishStatus
    image_url: Optional[str] = None  # shown on mobile menu for quick identification
    created_at: datetime
    updated_at: datetime

    @computed_field
    @property
    def tax(self) -> Decimal:
        return (self.price * TAX_RATE).quantize(Decimal("0.01"))

    @computed_field
    @property
    def total_price(self) -> Decimal:
        return (self.price + self.tax).quantize(Decimal("0.01"))

    def is_available(self) -> bool:
        return self.status.is_available()

    def set_status(self, status_type: DishStatusType, timestamp: datetime, description: str = "") -> None:
        self.status = DishStatus(type=status_type, description=description)
        self.updated_at = timestamp

    def mark_unavailable(self, timestamp: datetime, reason: str = "") -> None:
        self.set_status(DishStatusType.UNAVAILABLE, timestamp, reason)

    def mark_available(self, timestamp: datetime) -> None:
        self.set_status(DishStatusType.AVAILABLE, timestamp)

    def mark_out_of_stock(self, timestamp: datetime, reason: str = "") -> None:
        self.set_status(DishStatusType.OUT_OF_STOCK, timestamp, reason)
