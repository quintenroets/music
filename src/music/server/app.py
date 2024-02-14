import tbhandler
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from ..context import context

app = FastAPI()

origins = [f"http://localhost:{context.config.frontend_port}"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=origins,
    allow_headers=origins,
)


@app.exception_handler(Exception)
async def handler(_: Request, exc: Exception) -> PlainTextResponse:
    tbhandler.show(exit_after=False, repeat=False)
    return PlainTextResponse(str(exc), status_code=400)
