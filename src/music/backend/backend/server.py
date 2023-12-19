import tbhandler
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from ..client.response_types import ArtistInfo, Track
from . import artistmanager
from .artistmanager import DisplayArtist, DisplaySong

app = FastAPI()

origins = [f"http://localhost:{8080}"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=origins,
    allow_headers=origins,
)


@app.exception_handler(Exception)  # type: ignore
async def handler(_: Request, exc: Exception) -> PlainTextResponse:
    tbhandler.show(exit_after=False, repeat=False)
    return PlainTextResponse(str(exc), status_code=400)


@app.get("/newartist")
async def get(name: str) -> list[DisplayArtist]:
    return artistmanager.search_artists(name)


@app.get("/newsong")  # type: ignore[no-redef]
async def get(name: str) -> list[DisplaySong]:
    return artistmanager.search_song(name)


@app.get("/addartist")  # type: ignore[no-redef]
async def get(id: str, name: str) -> None:
    return artistmanager.add_artist(id, name)


@app.get("/addsong")  # type: ignore[no-redef]
async def get(id: str) -> None:
    return artistmanager.add_song(id)


@app.get("/changeartist")  # type: ignore[no-redef]
async def get(id: str) -> None:
    return artistmanager.change_artist(id)


@app.get("/recommendedartists")  # type: ignore[no-redef]
async def get() -> list[ArtistInfo]:
    return artistmanager.recommendations()


@app.get("/recommendedsongs")  # type: ignore[no-redef]
async def get() -> list[Track]:
    return artistmanager.song_recommendations()


@app.get("/artists")  # type: ignore[no-redef]
async def get() -> list[dict[str, str]]:
    return artistmanager.artists()
