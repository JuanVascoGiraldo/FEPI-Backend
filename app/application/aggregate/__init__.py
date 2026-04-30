from fastapi import APIRouter

from . import user
from . import group

router = APIRouter()

router.include_router(user.router, tags=["users"])
router.include_router(group.router, tags=["groups"])
