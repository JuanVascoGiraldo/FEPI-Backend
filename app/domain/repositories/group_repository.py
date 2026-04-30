from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.aggregate.group import Group


class GroupRepository(ABC):

    @abstractmethod
    async def get_by_id(self, group_id: UUID) -> Optional[Group]:
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Group]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Group]:
        pass

    @abstractmethod
    async def create(self, group: Group) -> None:
        pass

    @abstractmethod
    async def update(self, group: Group) -> None:
        pass
