from fastapi import APIRouter

from . import queries

router = APIRouter(prefix="/tables")

router.include_router(queries.router)
