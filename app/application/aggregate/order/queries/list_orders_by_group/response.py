from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID


class OrderItemResponse(BaseModel):
    id: UUID
    dish_id: UUID
    name: str
    unit_price: Decimal
    quantity: int
    specifications: List[str]
    status: int


class PaymentResponse(BaseModel):
    id: UUID
    amount: Decimal
    tip: Decimal
    email: str
    name: str
    payment_method: str
    payment_type: str
    status: str
    dish_ids: Optional[List[UUID]] = None
    created_at: datetime


class OrderResponse(BaseModel):
    id: UUID
    table_id: UUID
    table_number: str
    waiter_id: Optional[UUID] = None
    items: List[OrderItemResponse]
    payments: List[PaymentResponse]
    status: int
    notes: Optional[str] = None
    total: Decimal
    total_paid: Decimal
    total_pending: Decimal
    created_at: datetime
    updated_at: datetime


class Response(BaseModel):
    orders: List[OrderResponse]
