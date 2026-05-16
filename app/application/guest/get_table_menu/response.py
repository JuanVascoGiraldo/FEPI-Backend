from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID


class DishPublicResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    price: Decimal
    tax: Decimal
    total_price: Decimal
    category: int
    image_url: Optional[str] = None


class OrderItemPublicResponse(BaseModel):
    id: UUID
    name: str
    unit_price: Decimal
    quantity: int
    specifications: List[str]
    status: int


class ActiveOrderPublicResponse(BaseModel):
    id: UUID
    items: List[OrderItemPublicResponse]
    total: Decimal
    total_paid: Decimal
    total_pending: Decimal
    has_pending_request: bool
    created_at: datetime


class Response(BaseModel):
    table_id: UUID
    table_number: str
    table_description: Optional[str] = None
    group: str
    dishes: List[DishPublicResponse]
    active_order: Optional[ActiveOrderPublicResponse] = None
