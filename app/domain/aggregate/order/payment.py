from pydantic import BaseModel, EmailStr
from uuid import UUID
from decimal import Decimal
from typing import Dict, List, Optional
from datetime import datetime


class Payment(BaseModel):
    id: UUID
    amount: Decimal
    tip: Decimal = Decimal("0")
    email: EmailStr
    name: str = ""
    fiscal_info: Optional[str] = None
    payment_method: str = "cash"   # "cash" | "card"
    payment_type: str = "amount"   # "amount" | "items"
    status: str = "pending"        # "pending" | "confirmed"
    dish_ids: Optional[List[UUID]] = None
    item_quantities: Optional[Dict[str, int]] = None  # item_id_str -> qty paid
    created_at: datetime
