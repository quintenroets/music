from collections.abc import Awaitable, Callable

import tbhandler
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from ..context import context
from .routers import artists, songs


def create_app() -> FastAPI:
    app = FastAPI()

    origins = [f"http://localhost:{context.config.frontend_port}"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def exception_handling(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        try:
            response = await call_next(request)
        except Exception as exception:
            tbhandler.show(exit_after=False, repeat=False)
            response = PlainTextResponse(str(exception), status_code=500)
        return response

    routers = artists.app, songs.app
    for router in routers:
        app.include_router(router)
    return app
