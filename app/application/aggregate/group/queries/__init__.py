from fastapi import APIRouter

from . import list_groups

router = APIRouter(tags=["group-queries"])

router.include_router(list_groups.router)
