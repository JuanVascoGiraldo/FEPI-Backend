from fastapi import APIRouter

from . import list_dishes_by_group

router = APIRouter(tags=["dish-queries"])

router.include_router(list_dishes_by_group.router)
