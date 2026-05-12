import pytest

from app.application.aggregate.user.commands.create_superadmin.handler import Handler as CreateSuperadminHandler
from app.application.aggregate.user.commands.create_superadmin.request import Request as CreateSuperadminRequest
from app.application.aggregate.user.commands.create_admin.handler import Handler as CreateAdminHandler
from app.application.aggregate.user.commands.create_admin.request import Request as CreateAdminRequest
from app.application.aggregate.user.commands.login.handler import Handler as LoginHandler
from app.application.aggregate.user.commands.login.request import Request as LoginRequest
from app.domain.exceptions import UserNotFoundException, InvalidCredentialsException
from app.domain.aggregate.user.user_role import UserRole
from tests.conftest import make_meta, create_group_in_db


class TestLogin:
    async def test_superadmin_login_success(
        self, user_repository, session_repository, encryption_service, logger, timestamp
    ):
        create_handler = CreateSuperadminHandler(
            user_repository=user_repository,
            encryption_service=encryption_service,
            logger=logger,
        )
        await create_handler.handle(
            CreateSuperadminRequest(
                first_name="Alice",
                last_name="Admin",
                email="alice@example.com",
                password="secret123",
            ),
            timestamp,
        )

        login_handler = LoginHandler(
            user_repository=user_repository,
            session_repository=session_repository,
            encryption_service=encryption_service,
            logger=logger,
        )
        response = await login_handler.handle(
            LoginRequest(email="alice@example.com", password="secret123"),
            timestamp,
        )

        assert response.user_id is not None
        assert response.session_id is not None
        assert response.jwt is not None
        assert response.role == int(UserRole.SUPERADMIN)
        assert response.group is None

    async def test_admin_login_with_group_success(
        self, user_repository, group_repository, session_repository, encryption_service, logger, timestamp
    ):
        await create_group_in_db(group_repository, "restaurant-x")
        superadmin_session = make_meta(UserRole.SUPERADMIN)
        create_handler = CreateAdminHandler(
            user_repository=user_repository,
            group_repository=group_repository,
            encryption_service=encryption_service,
            logger=logger,
        )
        await create_handler.handle(
            CreateAdminRequest(
                first_name="Bob",
                last_name="Manager",
                email="bob@restaurant-x.com",
                password="pass456",
                group="restaurant-x",
            ),
            superadmin_session,
        )

        login_handler = LoginHandler(
            user_repository=user_repository,
            session_repository=session_repository,
            encryption_service=encryption_service,
            logger=logger,
        )
        response = await login_handler.handle(
            LoginRequest(email="bob@restaurant-x.com", password="pass456", group="restaurant-x"),
            timestamp,
        )

        assert response.role == int(UserRole.ADMIN)
        assert response.group == "restaurant-x"
        assert response.jwt is not None
        assert response.expiration_date is not None

    async def test_user_not_found_raises(
        self, user_repository, session_repository, encryption_service, logger, timestamp
    ):
        login_handler = LoginHandler(
            user_repository=user_repository,
            session_repository=session_repository,
            encryption_service=encryption_service,
            logger=logger,
        )
        with pytest.raises(UserNotFoundException):
            await login_handler.handle(
                LoginRequest(email="ghost@example.com", password="whatever"),
                timestamp,
            )

    async def test_wrong_password_raises(
        self, user_repository, session_repository, encryption_service, logger, timestamp
    ):
        create_handler = CreateSuperadminHandler(
            user_repository=user_repository,
            encryption_service=encryption_service,
            logger=logger,
        )
        await create_handler.handle(
            CreateSuperadminRequest(
                first_name="Alice",
                last_name="Admin",
                email="alice@example.com",
                password="correct-password",
            ),
            timestamp,
        )

        login_handler = LoginHandler(
            user_repository=user_repository,
            session_repository=session_repository,
            encryption_service=encryption_service,
            logger=logger,
        )
        with pytest.raises(InvalidCredentialsException):
            await login_handler.handle(
                LoginRequest(email="alice@example.com", password="wrong-password"),
                timestamp,
            )

    async def test_wrong_group_raises_user_not_found(
        self, user_repository, group_repository, session_repository, encryption_service, logger, timestamp
    ):
        await create_group_in_db(group_repository, "group-a")
        superadmin_session = make_meta(UserRole.SUPERADMIN)
        create_handler = CreateAdminHandler(
            user_repository=user_repository,
            group_repository=group_repository,
            encryption_service=encryption_service,
            logger=logger,
        )
        await create_handler.handle(
            CreateAdminRequest(
                first_name="Carol",
                last_name="Admin",
                email="carol@group-a.com",
                password="pass",
                group="group-a",
            ),
            superadmin_session,
        )

        login_handler = LoginHandler(
            user_repository=user_repository,
            session_repository=session_repository,
            encryption_service=encryption_service,
            logger=logger,
        )
        with pytest.raises(UserNotFoundException):
            await login_handler.handle(
                LoginRequest(email="carol@group-a.com", password="pass", group="group-b"),
                timestamp,
            )
