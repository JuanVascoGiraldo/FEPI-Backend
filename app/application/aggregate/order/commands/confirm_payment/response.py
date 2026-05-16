from uuid import UUID
from pydantic import BaseModel


class Response(BaseModel):
    order_id: UUID
    payment_id: UUID
    fully_paid: bool
    order_status: int
