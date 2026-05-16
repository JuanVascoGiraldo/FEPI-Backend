from fastapi import APIRouter

from . import user
from . import group
from . import order
from . import table
from . import dish
from . import events

router = APIRouter()

router.include_router(user.router, tags=["users"])
router.include_router(group.router, tags=["groups"])
router.include_router(order.router, tags=["orders"])
router.include_router(table.router, tags=["tables"])
router.include_router(dish.router, tags=["dishes"])
router.include_router(events.router, tags=["events"])
