from typing import Optional
from pydantic import BaseModel


class Request(BaseModel):
    number: str
    description: Optional[str] = None
