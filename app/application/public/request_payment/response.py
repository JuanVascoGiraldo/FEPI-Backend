from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class Response(BaseModel):
    payment_id: UUID
    amount: Decimal
    status: str
