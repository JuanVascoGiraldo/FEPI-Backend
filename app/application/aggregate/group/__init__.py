from fastapi import APIRouter

from . import commands
from . import queries

router = APIRouter(prefix="/groups")

router.include_router(queries.router)
router.include_router(commands.router)
