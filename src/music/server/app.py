from collections.abc import Awaitable, Callable

import powertrace
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from .routers import artists, songs


def create_app() -> FastAPI:
    app = FastAPI()
    configure_cors(app)
    configure_exception_handler(app)
    configure_routes(app)
    return app


def configure_routes(app: FastAPI) -> None:
    routers = artists.app, songs.app
    for router in routers:
        app.include_router(router)


def configure_exception_handler(app: FastAPI) -> None:
    @app.middleware("http")
    async def exception_handling(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        try:
            response = await call_next(request)
        except Exception as exception:  # noqa: BLE001
            powertrace.visualize_traceback(exit_after=False, repeat=False)
            response = PlainTextResponse(str(exception), status_code=500)
        return response


def configure_cors(app: FastAPI) -> None:
    origins = ["https://music.com", "http://localhost:8080"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_headers=["*"],
    )
