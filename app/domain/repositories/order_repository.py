from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.domain.aggregate.order import Order, OrderStatus


class OrderRepository(ABC):

    @abstractmethod
    async def get_by_id(self, order_id: UUID) -> Optional[Order]:
        pass

    @abstractmethod
    async def get_by_group(self, group: str) -> List[Order]:
        pass

    @abstractmethod
    async def get_by_table_id(self, table_id: UUID) -> List[Order]:
        pass

    @abstractmethod
    async def get_open_by_table(self, table_id: UUID) -> Optional[Order]:
        """Returns the single active order for a table, if any."""
        pass

    @abstractmethod
    async def get_by_group_and_status(self, group: str, status: OrderStatus) -> List[Order]:
        pass

    @abstractmethod
    async def create(self, order: Order) -> None:
        pass

    @abstractmethod
    async def update(self, order: Order) -> None:
        pass

    @abstractmethod
    async def delete(self, order_id: UUID) -> None:
        pass
