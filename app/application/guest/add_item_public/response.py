from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel
from typing import List
from uuid import UUID


class OrderItemPublicResponse(BaseModel):
    id: UUID
    name: str
    unit_price: Decimal
    quantity: int
    specifications: List[str]
    status: int


class Response(BaseModel):
    order_id: UUID
    items: List[OrderItemPublicResponse]
    total: Decimal
    created_at: datetime
