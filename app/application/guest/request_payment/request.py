from decimal import Decimal
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class Request(BaseModel):
    payment_type: str          # "amount" | "items"
    amount: Optional[Decimal] = None
    tip: Decimal = Decimal("0")
    item_ids: Optional[List[UUID]] = None
    item_quantities: Optional[Dict[str, int]] = None  # item_id_str -> qty to pay
    payment_method: str        # "cash" | "card"
    name: str
    email: EmailStr
    fiscal_info: Optional[str] = None
