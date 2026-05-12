import pytest
from datetime import datetime, timezone
from logging import getLogger
from uuid import uuid4

from app.config import Config
from app.domain.aggregate.group.group import Group
from app.domain.aggregate.user.user_role import UserRole
from app.domain.aggregate.value_objects.meta import Meta
from app.infrastructure.persistance.mongodb.clients.mongo_test_client import MongoTestClient
from app.infrastructure.persistance.mongodb.user_repository import UserRepositoryImpl
from app.infrastructure.persistance.mongodb.group_repository import GroupRepositoryImpl
from app.infrastructure.persistance.mongodb.session_repository import SessionRepositoryImpl
from app.infrastructure.services.test_encription_service import EncryptionServiceTestImpl


@pytest.fixture
def mongo_client():
    return MongoTestClient()


@pytest.fixture
def config():
    return Config(environment="test")


@pytest.fixture
def encryption_service():
    return EncryptionServiceTestImpl()


@pytest.fixture
def logger():
    return getLogger("test")


@pytest.fixture
def user_repository(mongo_client, config, encryption_service):
    return UserRepositoryImpl(mongo_client, config, encryption_service)


@pytest.fixture
def group_repository(mongo_client, config):
    return GroupRepositoryImpl(mongo_client, config)


@pytest.fixture
def session_repository(mongo_client, config, encryption_service):
    return SessionRepositoryImpl(mongo_client, config, encryption_service)


@pytest.fixture
def timestamp():
    return datetime.now(timezone.utc)


def make_meta(role: UserRole, group: str = "") -> Meta:
    return Meta(
        user_id=uuid4(),
        session_id=uuid4(),
        role=role,
        group=group,
        timestamp=datetime.now(timezone.utc),
        jwt="test-jwt",
    )


async def create_group_in_db(group_repository, name: str) -> Group:
    now = datetime.now(timezone.utc)
    group = Group(id=uuid4(), name=name, is_active=True, created_at=now, updated_at=now)
    await group_repository.create(group)
    return group
