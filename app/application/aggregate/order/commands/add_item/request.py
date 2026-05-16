from pydantic import BaseModel, Field
from typing import List
from uuid import UUID


class Request(BaseModel):
    dish_id: UUID
    quantity: int = Field(default=1, ge=1)
    specifications: List[str] = Field(default_factory=list)
