from fastapi import APIRouter

from . import create_group
from . import delete_group

router = APIRouter(tags=["group-commands"])

router.include_router(create_group.router)
router.include_router(delete_group.router)
