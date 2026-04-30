from typing import List, Optional
from uuid import UUID

from app.config import Config
from app.domain.aggregate.group import Group
from app.domain.repositories.group_repository import GroupRepository
from app.infrastructure.persistance.mongodb.clients import MongoClient
from app.infrastructure.persistance.mongodb.dao.group_dao import GroupDao
from app.infrastructure.persistance.mongodb.mappers.group import from_dao_to_group, from_group_to_dao

NAME_PK_PREFIX = "GROUP_NAME#"
GROUP_SK_PREFIX = "GROUP#"


class GroupRepositoryImpl(GroupRepository):
    COLLECTION = "groups"
    INDEX_COLLECTION = "indexes"

    def __init__(self, mongo_client: MongoClient, config: Config) -> None:
        self.mongo_client = mongo_client
        self.config = config

    async def get_by_id(self, group_id: UUID) -> Optional[Group]:
        document = await self.mongo_client.find_one(
            self.COLLECTION,
            {"pk": f"{GroupDao.PK}{group_id}", "sk": GroupDao.SK},
        )
        if document is None:
            return None
        return from_dao_to_group(GroupDao.from_document(document))

    async def get_by_name(self, name: str) -> Optional[Group]:
        document = await self.mongo_client.find_one(
            self.COLLECTION,
            {"sk": GroupDao.SK, "name": name},
        )
        if document is None:
            return None
        return from_dao_to_group(GroupDao.from_document(document))

    async def get_all(self) -> List[Group]:
        documents = await self.mongo_client.find_many(
            self.COLLECTION,
            {"sk": GroupDao.SK},
        )
        return [from_dao_to_group(GroupDao.from_document(d)) for d in documents]

    async def create(self, group: Group) -> None:
        dao = from_group_to_dao(group)
        document = dao.to_document()
        document["entity"] = "GROUP"
        await self.mongo_client.insert_one(self.COLLECTION, document)

    async def update(self, group: Group) -> None:
        dao = from_group_to_dao(group)
        update_fields = dao.model_dump(mode="json", exclude={"pk", "sk"})
        await self.mongo_client.update_one(
            self.COLLECTION,
            {"pk": f"{GroupDao.PK}{group.id}", "sk": GroupDao.SK},
            update_fields,
        )
