import pytest

from app.application.aggregate.user.commands.create_superadmin.handler import Handler as CreateSuperadminHandler
from app.application.aggregate.user.commands.create_superadmin.request import Request as CreateSuperadminRequest
from app.application.aggregate.user.commands.create_admin.handler import Handler as CreateAdminHandler
from app.application.aggregate.user.commands.create_admin.request import Request as CreateAdminRequest
from app.application.aggregate.user.commands.create_waiter.handler import Handler as CreateWaiterHandler
from app.application.aggregate.user.commands.create_waiter.request import Request as CreateWaiterRequest
from app.domain.exceptions import (
    EmailAlreadyExistsException,
    IsNotAuthorizedException,
    GroupNotFoundException,
)
from app.domain.aggregate.user.user_role import UserRole
from tests.conftest import make_meta, create_group_in_db


class TestCreateSuperadmin:
    async def test_success(self, user_repository, encryption_service, logger, timestamp):
        handler = CreateSuperadminHandler(
            user_repository=user_repository,
            encryption_service=encryption_service,
            logger=logger,
        )
        request = CreateSuperadminRequest(
            first_name="Alice",
            last_name="Admin",
            email="alice@example.com",
            password="secret123",
        )
        response = await handler.handle(request, timestamp)

        assert response.email == "alice@example.com"
        assert response.first_name == "Alice"
        assert response.last_name == "Admin"
        assert response.role == int(UserRole.SUPERADMIN)
        assert response.group is None
        assert response.is_active is True
        assert response.id is not None

    async def test_duplicate_email_raises(self, user_repository, encryption_service, logger, timestamp):
        handler = CreateSuperadminHandler(
            user_repository=user_repository,
            encryption_service=encryption_service,
            logger=logger,
        )
        request = CreateSuperadminRequest(
            first_name="Alice",
            last_name="Admin",
            email="alice@example.com",
            password="secret123",
        )
        await handler.handle(request, timestamp)

        with pytest.raises(EmailAlreadyExistsException):
            await handler.handle(request, timestamp)


class TestCreateAdmin:
    async def test_success(self, user_repository, group_repository, encryption_service, logger):
        await create_group_in_db(group_repository, "restaurant-a")
        session = make_meta(UserRole.SUPERADMIN)
        handler = CreateAdminHandler(
            user_repository=user_repository,
            group_repository=group_repository,
            encryption_service=encryption_service,
            logger=logger,
        )
        request = CreateAdminRequest(
            first_name="Bob",
            last_name="Manager",
            email="bob@restaurant-a.com",
            password="pass456",
            group="restaurant-a",
        )
        response = await handler.handle(request, session)

        assert response.email == "bob@restaurant-a.com"
        assert response.first_name == "Bob"
        assert response.role == int(UserRole.ADMIN)
        assert response.group == "restaurant-a"
        assert response.is_active is True

    async def test_unauthorized_when_not_superadmin(
        self, user_repository, group_repository, encryption_service, logger
    ):
        session = make_meta(UserRole.ADMIN, group="restaurant-a")
        handler = CreateAdminHandler(
            user_repository=user_repository,
            group_repository=group_repository,
            encryption_service=encryption_service,
            logger=logger,
        )
        request = CreateAdminRequest(
            first_name="Bob",
            last_name="Manager",
            email="bob@example.com",
            password="pass456",
            group="restaurant-a",
        )
        with pytest.raises(IsNotAuthorizedException):
            await handler.handle(request, session)

    async def test_group_not_found_raises(
        self, user_repository, group_repository, encryption_service, logger
    ):
        session = make_meta(UserRole.SUPERADMIN)
        handler = CreateAdminHandler(
            user_repository=user_repository,
            group_repository=group_repository,
            encryption_service=encryption_service,
            logger=logger,
        )
        request = CreateAdminRequest(
            first_name="Bob",
            last_name="Manager",
            email="bob@example.com",
            password="pass456",
            group="nonexistent-group",
        )
        with pytest.raises(GroupNotFoundException):
            await handler.handle(request, session)

    async def test_duplicate_email_in_group_raises(
        self, user_repository, group_repository, encryption_service, logger
    ):
        await create_group_in_db(group_repository, "restaurant-b")
        session = make_meta(UserRole.SUPERADMIN)
        handler = CreateAdminHandler(
            user_repository=user_repository,
            group_repository=group_repository,
            encryption_service=encryption_service,
            logger=logger,
        )
        request = CreateAdminRequest(
            first_name="Carol",
            last_name="Manager",
            email="carol@restaurant-b.com",
            password="pass789",
            group="restaurant-b",
        )
        await handler.handle(request, session)

        with pytest.raises(EmailAlreadyExistsException):
            await handler.handle(request, session)


class TestCreateWaiter:
    async def test_success(self, user_repository, group_repository, encryption_service, logger):
        await create_group_in_db(group_repository, "restaurant-c")
        session = make_meta(UserRole.ADMIN, group="restaurant-c")
        handler = CreateWaiterHandler(
            user_repository=user_repository,
            group_repository=group_repository,
            encryption_service=encryption_service,
            logger=logger,
        )
        request = CreateWaiterRequest(
            first_name="Dan",
            last_name="Waiter",
            email="dan@restaurant-c.com",
            password="pass000",
            group="restaurant-c",
        )
        response = await handler.handle(request, session)

        assert response.email == "dan@restaurant-c.com"
        assert response.first_name == "Dan"
        assert response.role == int(UserRole.WAITER)
        assert response.group == "restaurant-c"
        assert response.is_active is True

    async def test_unauthorized_when_not_admin(
        self, user_repository, group_repository, encryption_service, logger
    ):
        session = make_meta(UserRole.SUPERADMIN)
        handler = CreateWaiterHandler(
            user_repository=user_repository,
            group_repository=group_repository,
            encryption_service=encryption_service,
            logger=logger,
        )
        request = CreateWaiterRequest(
            first_name="Dan",
            last_name="Waiter",
            email="dan@example.com",
            password="pass000",
            group="restaurant-c",
        )
        with pytest.raises(IsNotAuthorizedException):
            await handler.handle(request, session)

    async def test_unauthorized_when_different_group(
        self, user_repository, group_repository, encryption_service, logger
    ):
        await create_group_in_db(group_repository, "restaurant-d")
        session = make_meta(UserRole.ADMIN, group="restaurant-other")
        handler = CreateWaiterHandler(
            user_repository=user_repository,
            group_repository=group_repository,
            encryption_service=encryption_service,
            logger=logger,
        )
        request = CreateWaiterRequest(
            first_name="Dan",
            last_name="Waiter",
            email="dan@example.com",
            password="pass000",
            group="restaurant-d",
        )
        with pytest.raises(IsNotAuthorizedException):
            await handler.handle(request, session)

    async def test_duplicate_email_in_group_raises(
        self, user_repository, group_repository, encryption_service, logger
    ):
        await create_group_in_db(group_repository, "restaurant-e")
        session = make_meta(UserRole.ADMIN, group="restaurant-e")
        handler = CreateWaiterHandler(
            user_repository=user_repository,
            group_repository=group_repository,
            encryption_service=encryption_service,
            logger=logger,
        )
        request = CreateWaiterRequest(
            first_name="Eve",
            last_name="Waiter",
            email="eve@restaurant-e.com",
            password="pass111",
            group="restaurant-e",
        )
        await handler.handle(request, session)

        with pytest.raises(EmailAlreadyExistsException):
            await handler.handle(request, session)
