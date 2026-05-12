from fastapi import APIRouter

from . import queries

router = APIRouter(prefix="/orders")

router.include_router(queries.router)
