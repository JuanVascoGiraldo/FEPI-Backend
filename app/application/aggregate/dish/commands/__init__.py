from fastapi import APIRouter

from . import create_dish

router = APIRouter(tags=["dish-commands"])

router.include_router(create_dish.router)
