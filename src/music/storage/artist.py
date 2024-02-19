from __future__ import annotations

import typing

from package_utils.storage import CachedFileContent

from ..models import Artist
from .artist_paths import Paths


class StorageModel:
    albums: dict[str, dict[str, str]]
    albums_count: int
    album_counts: dict[str, int]
    top_tracks: dict[str, str]

    def __init__(self, artist: Artist) -> None:
        self.artist = artist

    def get_album_count(self, album_type: str) -> int:
        return self.album_counts.get(album_type, 0)

    def set_album_count(self, album_type: str, value: int) -> None:
        self.album_counts[album_type] = value

    def add_album_count(self, album_type: str, value: int) -> None:
        new_count = self.get_album_count(album_type) + value
        self.set_album_count(album_type, new_count)


class Storage(StorageModel):
    def __new__(cls, artist: Artist) -> Storage:
        paths = Paths(artist)

        class ImplementedStorage(StorageModel):
            albums = paths.albums.cached_content  # type: ignore
            albums_count = CachedFileContent(paths.albums_count, default=0)  # type: ignore
            album_counts = paths.album_counts.cached_content  # type: ignore
            top_tracks = paths.top_tracks.cached_content

        storage = ImplementedStorage(artist)
        return typing.cast(Storage, storage)
