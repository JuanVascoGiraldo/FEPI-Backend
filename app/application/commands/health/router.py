from app.dependencies import get_dependency
from fastapi import APIRouter, status, Depends
from .handler import Handler
from .request import Request
from .response import Response

router = APIRouter()


@router.get("/health", response_model=Response, status_code=status.HTTP_200_OK)
async def health(request: Request = Depends()):
    handler: Handler = get_dependency(Handler)
    return await handler.handle(request)
