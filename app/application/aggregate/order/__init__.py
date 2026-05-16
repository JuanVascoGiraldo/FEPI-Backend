from fastapi import APIRouter

from . import queries, commands

router = APIRouter(prefix="/orders")

router.include_router(queries.router)
router.include_router(commands.router)
