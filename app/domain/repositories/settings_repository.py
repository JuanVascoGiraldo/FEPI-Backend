from abc import ABC, abstractmethod
from typing import Optional
from app.domain.aggregate.settings.group_settings import GroupSettings


class SettingsRepository(ABC):
    @abstractmethod
    async def get_by_group(self, group: str) -> Optional[GroupSettings]:
        pass

    @abstractmethod
    async def upsert(self, settings: GroupSettings) -> None:
        pass
