from fastapi import APIRouter, status
from uuid import UUID

from app.dependencies import get_dependency

from .handler import Handler

router = APIRouter()


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(group_id: UUID):
    handler: Handler = get_dependency(Handler)
    await handler.handle(group_id)
