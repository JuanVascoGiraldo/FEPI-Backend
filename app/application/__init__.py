from fastapi import APIRouter

from . import aggregate
from . import commands
from . import public

router = APIRouter(prefix="/api")

router.include_router(commands.router)
router.include_router(aggregate.router)
router.include_router(public.router)
