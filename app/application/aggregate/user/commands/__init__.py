from fastapi import APIRouter

from . import create_superadmin
from . import create_admin
from . import create_waiter
from . import login

router = APIRouter(tags=["user-commands"])

router.include_router(create_superadmin.router)
router.include_router(create_admin.router)
router.include_router(create_waiter.router)
router.include_router(login.router)
