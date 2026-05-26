from pydantic import BaseModel
from typing import Optional


class GroupSettings(BaseModel):
    group: str
    restaurant_name: Optional[str] = None
    logo_url: Optional[str] = None
    primary_color: str = "#f59e0b"
