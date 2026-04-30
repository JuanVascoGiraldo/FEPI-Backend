from fastapi import APIRouter

from . import aggregate
from . import commands

router = APIRouter(prefix="/api")

router.include_router(commands.router)
router.include_router(aggregate.router)
