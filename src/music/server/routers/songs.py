from typing import Any

from fastapi import APIRouter

from ...context import context
from ...models.response_types import Track
from ..servers.songs import Server

app = APIRouter(prefix="/songs")
server = Server()


@app.get("/search")
async def search_song(name: str) -> list[dict[str, Any]]:
    songs = server.create_song_search_results(name)
    return list(songs)


@app.get("/add")
async def save_new_track(id: str) -> None:
    songs = context.spotify_client.songs([id])
    context.storage.save_new_tracks(songs)


@app.get("/recommendations")
async def recommend_songs() -> list[Track]:
    songs = server.create_song_recommendations()
    return list(songs)
