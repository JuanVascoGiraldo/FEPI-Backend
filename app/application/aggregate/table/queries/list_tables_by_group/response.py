from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from uuid import UUID


class PaymentResponse(BaseModel):
    id: UUID
    amount: Decimal
    tip: Decimal
    email: EmailStr
    dish_ids: Optional[List[UUID]] = None
    created_at: datetime


class OrderItemResponse(BaseModel):
    id: UUID
    dish_id: UUID
    name: str
    unit_price: Decimal
    quantity: int
    specifications: List[str]
    status: int


class ActiveOrderResponse(BaseModel):
    id: UUID
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


class TableResponse(BaseModel):
    id: UUID
    number: str
    capacity: int
    description: Optional[str] = None
    status: int
    active_order: Optional[ActiveOrderResponse] = None
    created_at: datetime
    updated_at: datetime


class Response(BaseModel):
    tables: List[TableResponse]
