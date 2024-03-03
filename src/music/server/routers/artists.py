from typing import Any

from fastapi import APIRouter

from ...context import context
from ...models import Artist
from ...models.response_types import ArtistInfo
from ..servers.artists import Server

app = APIRouter(prefix="/artists")
server = Server()


@app.get("")
async def load_saved_artists() -> list[dict[str, Any]]:
    artists = server.load_saved_artists()
    return list(artists)


@app.get("/search")
async def search_artist(name: str) -> list[dict[str, Any]]:
    artists = server.create_artist_search_results(name)
    return list(artists)


@app.get("/add")
async def save_new_artist(id: str, name: str) -> None:
    artist = Artist(id, name)
    return context.storage.save_new_artist(artist)


@app.get("/toggle")
async def toggle_artist_type(id: str) -> None:
    artists: list[Artist] = context.storage.artists
    for artist in artists:
        if artist.id == id:
            artist.toggle_type()
    context.storage.artists = artists


@app.get("/recommendations")
async def recommend_artists() -> list[ArtistInfo]:
    return server.create_artist_recommendations()
