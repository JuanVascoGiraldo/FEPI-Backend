from pydantic import BaseModel

from .dish_status_type import DishStatusType


class DishStatus(BaseModel):
    """
    Pairs a status type with a human-readable description so that
    the waiter or admin can communicate exactly why a dish is unavailable
    (e.g. "Main ingredient ran out", "Only available on weekends").
    """

    type: DishStatusType
    description: str = ""

    def is_available(self) -> bool:
        return self.type == DishStatusType.AVAILABLE
