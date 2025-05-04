from typing import Any

from fastapi import APIRouter

from music.models.response_types import Track
from music.runtime import runtime
from music.server.servers.songs import Server

app = APIRouter(prefix="/songs")
server = Server()


@app.get("/search")
async def search_song(name: str) -> list[dict[str, Any]]:
    songs = server.create_song_search_results(name)
    return list(songs)


@app.get("/search/youtube")
async def search_song_youtube(name: str) -> list[dict[str, Any]]:
    songs = server.create_youtube_search_results(name)
    return list(songs)


@app.get("/add")
async def save_new_track(id_: str, *, youtube: bool = False) -> None:
    if youtube:
        runtime.storage.add_youtube_track_to_download(id_)
    else:
        songs = runtime.spotify_client.songs([id_])
        runtime.storage.save_new_tracks(songs)


@app.get("/recommendations")
async def recommend_songs() -> list[Track]:
    songs = server.create_song_recommendations()
    return list(songs)
