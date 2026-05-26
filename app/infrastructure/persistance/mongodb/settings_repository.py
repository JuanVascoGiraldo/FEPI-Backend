from typing import Optional
from app.domain.aggregate.settings.group_settings import GroupSettings
from app.domain.repositories.settings_repository import SettingsRepository
from app.infrastructure.persistance.mongodb.clients import MongoClient

COLLECTION = "group_settings"


class SettingsRepositoryImpl(SettingsRepository):
    def __init__(self, client: MongoClient) -> None:
        self.client = client

    async def get_by_group(self, group: str) -> Optional[GroupSettings]:
        doc = await self.client.db[COLLECTION].find_one({"pk": group})
        if not doc:
            return None
        return GroupSettings(
            group=group,
            restaurant_name=doc.get("restaurant_name"),
            logo_url=doc.get("logo_url"),
            primary_color=doc.get("primary_color", "#f59e0b"),
        )

    async def upsert(self, settings: GroupSettings) -> None:
        await self.client.db[COLLECTION].update_one(
            {"pk": settings.group},
            {"$set": {
                "pk": settings.group,
                "restaurant_name": settings.restaurant_name,
                "logo_url": settings.logo_url,
                "primary_color": settings.primary_color,
            }},
            upsert=True,
        )
