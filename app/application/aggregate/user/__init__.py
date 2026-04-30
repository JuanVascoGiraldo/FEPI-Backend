from fastapi import APIRouter
from . import commands
from . import queries

router = APIRouter(prefix="/users")

router.include_router(commands.router)
router.include_router(queries.router)
