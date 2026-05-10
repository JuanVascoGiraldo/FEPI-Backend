from typing import List, Optional
from uuid import UUID

from app.config import Config
from app.domain.aggregate.user import User, UserRole
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.persistance.mongodb.clients import MongoClient
from app.infrastructure.persistance.mongodb.dao.user_dao import UserDao
from app.infrastructure.persistance.mongodb.dao.index_dao import IndexDao
from app.infrastructure.persistance.mongodb.mappers.user import from_dao_to_user, from_user_to_dao

GROUP_EMAIL_PK_PREFIX = "GROUP_EMAIL#"
USER_SK_PREFIX = "USER#"


class UserRepositoryImpl(UserRepository):
    COLLECTION = "users"
    INDEX_COLLECTION = "indexes"

    def __init__(self, mongo_client: MongoClient, config: Config) -> None:
        self.mongo_client = mongo_client
        self.config = config

    def _group_email_index(self, group: Optional[str], email: str, user_id: UUID) -> IndexDao:
        return IndexDao(
            pk=f"{GROUP_EMAIL_PK_PREFIX}{group or ''}:{email.lower()}",
            sk=f"{USER_SK_PREFIX}{user_id}",
        )

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        document = await self.mongo_client.find_one(
            self.COLLECTION,
            {"pk": f"{UserDao.PK}{user_id}", "sk": UserDao.SK},
        )
        if document is None:
            return None
        return from_dao_to_user(UserDao.from_document(document))

    async def get_by_email(self, email: str) -> Optional[User]:
        document = await self.mongo_client.find_one(
            self.COLLECTION,
            {"sk": UserDao.SK, "email": email.lower()},
        )
        if document is None:
            return None
        return from_dao_to_user(UserDao.from_document(document))

    async def get_by_group_and_email(self, group: Optional[str], email: str) -> Optional[User]:
        index = await self.mongo_client.find_one(
            self.INDEX_COLLECTION,
            {"pk": f"{GROUP_EMAIL_PK_PREFIX}{group or ''}:{email.lower()}"},
        )
        if index is None:
            return None
        user_id = UUID(index["sk"].replace(USER_SK_PREFIX, "", 1))
        return await self.get_by_id(user_id)

    async def get_by_group(self, group: str) -> List[User]:
        documents = await self.mongo_client.find_many(
            self.COLLECTION,
            {"sk": UserDao.SK, "group": group},
        )
        return [from_dao_to_user(UserDao.from_document(d)) for d in documents]

    async def get_by_group_and_role(self, group: str, role: UserRole) -> List[User]:
        documents = await self.mongo_client.find_many(
            self.COLLECTION,
            {"sk": UserDao.SK, "group": group, "role": int(role)},
        )
        return [from_dao_to_user(UserDao.from_document(d)) for d in documents]

    async def get_by_role(self, role: UserRole) -> List[User]:
        documents = await self.mongo_client.find_many(
            self.COLLECTION,
            {"sk": UserDao.SK, "role": int(role)},
        )
        return [from_dao_to_user(UserDao.from_document(d)) for d in documents]

    async def create(self, user: User) -> None:
        dao = from_user_to_dao(user)
        document = dao.to_document()
        document["entity"] = "USER"
        await self.mongo_client.insert_one(self.COLLECTION, document)

        group_email_index = self._group_email_index(user.group, user.email.value, user.id)
        index_doc = group_email_index.to_document()
        index_doc["entity"] = "USER_GROUP_EMAIL_INDEX"
        await self.mongo_client.insert_one(self.INDEX_COLLECTION, index_doc)

    async def update(self, user: User) -> None:
        dao = from_user_to_dao(user)
        update_fields = dao.model_dump(mode="json", exclude={"pk", "sk"})
        await self.mongo_client.update_one(
            self.COLLECTION,
            {"pk": f"{UserDao.PK}{user.id}", "sk": UserDao.SK},
            update_fields,
        )

    async def delete(self, user_id: UUID) -> None:
        user = await self.get_by_id(user_id)
        await self.mongo_client.delete_one(
            self.COLLECTION,
            {"pk": f"{UserDao.PK}{user_id}", "sk": UserDao.SK},
        )
        if user:
            await self.mongo_client.delete_one(
                self.INDEX_COLLECTION,
                {"pk": f"{GROUP_EMAIL_PK_PREFIX}{user.group or ''}:{user.email.value.lower()}"},
            )
