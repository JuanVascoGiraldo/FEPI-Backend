from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class Response(BaseModel):
    id: UUID
    group: str
    name: str
    description: str
    price: Decimal
    tax: Decimal
    total_price: Decimal
    category: int
    status: int
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
