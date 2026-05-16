from uuid import UUID

from fastapi import APIRouter, status

from app.dependencies import get_dependency

from .handler import Handler
from .request import Request
from .response import Response

router = APIRouter()


@router.post("/table/{table_id}/payment", response_model=Response, status_code=status.HTTP_201_CREATED)
async def request_payment(table_id: UUID, body: Request) -> Response:
    handler: Handler = get_dependency(Handler)
    return await handler.handle(table_id, body)
