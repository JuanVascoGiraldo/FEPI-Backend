from fastapi import APIRouter

from . import create_superadmin
from . import create_admin
from . import create_waiter
from . import login
from . import change_password
from . import forgot_password
from . import reset_password

router = APIRouter(tags=["user-commands"])

router.include_router(create_superadmin.router)
router.include_router(create_admin.router)
router.include_router(create_waiter.router)
router.include_router(login.router)
router.include_router(change_password.router)
router.include_router(forgot_password.router)
router.include_router(reset_password.router)
