from fastapi import APIRouter, Depends, status

from app.dependencies import get_dependency
from app.infrastructure.inyections import get_utc_timestamp

from .handler import Handler
from .request import Request
from .response import Response

router = APIRouter()


@router.post("/forgot-password", response_model=Response, status_code=status.HTTP_200_OK)
async def forgot_password(
    request: Request, timestamp=Depends(get_utc_timestamp)
) -> Response:
    handler: Handler = get_dependency(Handler)
    return await handler.handle(request, timestamp)
