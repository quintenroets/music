from typing import Annotated, Any

from fastapi import APIRouter, Depends

from music.context import context
from music.models import Artist
from music.models.response_types import ArtistInfo
from music.server.servers.artists import Server

app = APIRouter(prefix="/artists")
server = Server()


def parse_limit(limit: str | None = None) -> int | None:
    if limit is None:
        parsed_limit = 20
    elif not limit:
        parsed_limit = None
    else:
        parsed_limit = int(limit)
    return parsed_limit


@app.get("")
async def load_saved_artists(
    offset: int = 0,
    limit: Annotated[int | None, Depends(parse_limit)] = None,
) -> list[dict[str, Any]]:
    artists = server.load_saved_artists(offset=offset, limit=limit)
    return list(artists)


@app.get("/search")
async def search_artist(name: str) -> list[dict[str, Any]]:
    artists = server.create_artist_search_results(name)
    return list(artists)


@app.get("/add")
async def save_new_artist(id_: str, name: str) -> None:
    artist = Artist(id_, name)
    return context.storage.save_new_artist(artist)


@app.get("/toggle")
async def toggle_artist_type(id_: str) -> None:
    artists: list[Artist] = context.storage.artists
    for artist in artists:
        if artist.id == id_:
            artist.toggle_type()
    context.storage.artists = artists


@app.get("/recommendations")
async def recommend_artists() -> list[ArtistInfo]:
    return server.create_artist_recommendations()
