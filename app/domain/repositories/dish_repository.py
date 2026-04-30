from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.domain.aggregate.dish import Dish, FoodCategory


class DishRepository(ABC):

    @abstractmethod
    async def get_by_id(self, dish_id: UUID) -> Optional[Dish]:
        pass

    @abstractmethod
    async def get_by_group(self, group: str) -> List[Dish]:
        pass

    @abstractmethod
    async def get_available_by_group(self, group: str) -> List[Dish]:
        pass

    @abstractmethod
    async def get_by_group_and_category(self, group: str, category: FoodCategory) -> List[Dish]:
        pass

    @abstractmethod
    async def create(self, dish: Dish) -> None:
        pass

    @abstractmethod
    async def update(self, dish: Dish) -> None:
        pass

    @abstractmethod
    async def delete(self, dish_id: UUID) -> None:
        pass
