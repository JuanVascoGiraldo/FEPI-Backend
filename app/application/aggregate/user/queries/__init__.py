from fastapi import APIRouter

from . import list_admins, list_waiters

router = APIRouter(tags=["user-queries"])

router.include_router(list_admins.router)
router.include_router(list_waiters.router)
