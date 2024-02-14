from typing import Any

from ..context import context
from ..models import Artist
from ..models.response_types import ArtistInfo, Track
from .app import app
from .server import Server

backend = Server()


@app.get("/newartist")
async def get(name: str) -> list[dict[str, Any]]:
    artists = backend.create_artist_search_results(name)
    return list(artists)


@app.get("/newsong")  # type: ignore[no-redef]
async def get(name: str) -> list[dict[str, Any]]:
    songs = backend.create_song_search_results(name)
    return list(songs)


@app.get("/addartist")  # type: ignore[no-redef]
async def get(id: str, name: str) -> None:
    artist = Artist(id, name)
    return context.storage.save_new_artist(artist)


@app.get("/addsong")  # type: ignore[no-redef]
async def get(id: str) -> None:
    songs = context.spotify_client.songs([id])
    context.storage.save_new_tracks(songs)


@app.get("/changeartist")  # type: ignore[no-redef]
async def get(id: str) -> None:
    artists = context.storage.artists
    for artist in artists:
        if artist.id == id:
            artist.toggle_type()
    context.storage.artists = artists


@app.get("/recommendedartists")  # type: ignore[no-redef]
async def get() -> list[ArtistInfo]:
    return backend.create_artist_recommendations()


@app.get("/recommendedsongs")  # type: ignore[no-redef]
async def get() -> list[Track]:
    songs = backend.create_song_recommendations()
    return list(songs)


@app.get("/artists")  # type: ignore[no-redef]
async def get() -> list[dict[str, str]]:
    artists = backend.load_saved_artists()
    return list(artists)
