from fastapi import APIRouter

from . import list_admins

router = APIRouter(tags=["user-queries"])

router.include_router(list_admins.router)
