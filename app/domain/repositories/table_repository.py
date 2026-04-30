from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.domain.aggregate.table import Table, TableStatus


class TableRepository(ABC):

    @abstractmethod
    async def get_by_id(self, table_id: UUID) -> Optional[Table]:
        pass

    @abstractmethod
    async def get_by_group(self, group: str) -> List[Table]:
        pass

    @abstractmethod
    async def get_by_group_and_status(self, group: str, status: TableStatus) -> List[Table]:
        pass

    @abstractmethod
    async def create(self, table: Table) -> None:
        pass

    @abstractmethod
    async def update(self, table: Table) -> None:
        pass

    @abstractmethod
    async def delete(self, table_id: UUID) -> None:
        pass
