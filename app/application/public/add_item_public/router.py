from uuid import UUID

from fastapi import APIRouter, status

from app.dependencies import get_dependency

from .handler import Handler
from .request import Request
from .response import Response

router = APIRouter()


@router.post("/table/{table_id}/order/items", response_model=Response, status_code=status.HTTP_200_OK)
async def add_item_public(table_id: UUID, body: Request) -> Response:
    handler: Handler = get_dependency(Handler)
    return await handler.handle(table_id, body)
