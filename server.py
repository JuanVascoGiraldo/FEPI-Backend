from app.infrastructure.middlewares import ErrorMiddleWare, ContextMiddleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from app.logger import configure_logging
from app.config import get_settings
from app.application import router
from fastapi import FastAPI, APIRouter


def create_app(on_shutdown=None, on_startup=None):
    configure_logging()
    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
    ]
    middlewares = [
        Middleware(CORSMiddleware,
                   allow_origins=allowed_origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   expose_headers=[
                       "Access-Control-Allow-Headers",
                       "X-Process-Time",
                   ]),
        Middleware(ContextMiddleware),
        Middleware(ErrorMiddleWare),
    ]
    if not on_shutdown:
        on_shutdown = []
    if not on_startup:
        on_startup = []
    on_startup.extend([])
    app = FastAPI(
        title=get_settings().app_name,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        middleware=middlewares,
        openapi_url=get_settings().get_open_api_path(),
    )

    app.include_router(router)
    api_router = APIRouter(prefix="/api")
    api_router.include_router(router)
    app.include_router(api_router)
    return app


app = create_app()


if __name__ == "__main__":
    from uvicorn import run
    run("server:app", host=get_settings().host, port=get_settings().port,
        server_header=False, date_header=False,
        reload=get_settings().get_reload(), workers=get_settings().workers)
