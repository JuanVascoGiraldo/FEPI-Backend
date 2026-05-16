from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class Request(BaseModel):
    name: str
    description: str
    price: Decimal
    category: int
    image_url: Optional[str] = None
