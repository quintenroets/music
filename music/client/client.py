import functools
from collections.abc import Callable
from typing import Any, TypeVar

from . import _client
from .response_types import (
    Album,
    Albums,
    AlbumTrack,
    AlbumTracks,
    ArtistInfo,
    Artists,
    ArtistSearch,
    RecommendedTracks,
    Track,
    Tracks,
    TrackSearch,
)

T = TypeVar("T")


def combine_chunks(f: Callable[..., list[T]]) -> Callable[..., list[T]]:
    """
    Combine function calls on chunks instead of whole array in one time :return: All
    results of the chunks.
    """

    @functools.wraps(f)
    def chunked_wrapper(*args: Any, **kwargs: Any) -> list[T]:
        self, items, *args_tuple = args

        @combine_offsets
        def calculate_chunk(self: Any, offset: int, limit: int) -> list[T]:
            return f(self, items[offset : offset + limit], *args_tuple, **kwargs)

        return calculate_chunk(self, len(items))

    return chunked_wrapper


def combine_offsets(
    f: Callable[..., list[T]], chunk_size: int = 50
) -> Callable[..., list[T]]:
    """
    Combine function calls with offset and limit instead of total amount :param
    chunk_size: Size of the chunks :return: All results of the chunks.
    """

    def chunked_wrapper(self: Any, amount: int, *args: Any, **kwargs: Any) -> list[T]:
        return [
            item
            for offset in range(0, amount, chunk_size)
            for item in f(self, *args, offset=offset, limit=chunk_size, **kwargs)
        ]

    return chunked_wrapper


class SpotApi:
    def __init__(self) -> None:
        self.api = _client.Spotify()

    def search_song(self, name: str) -> list[Track]:
        songs = self.api.search(name, type="track")
        return TrackSearch.from_dict(songs["tracks"]).items

    def search_artist(self, name: str) -> list[ArtistInfo]:
        artists = self.api.search(name, type="artist")
        return ArtistSearch.from_dict(artists["artists"]).items

    @combine_chunks
    def artists(self, ids: str) -> list[ArtistInfo]:
        artists = self.api.artists(ids)
        return Artists.from_dict(artists).artists

    def related_artists(self, id: str) -> list[ArtistInfo]:
        artists = self.api.artist_related_artists(id)
        return Artists.from_dict(artists).artists

    def song_recommendations(self, track_ids: list[str]) -> list[Track]:
        songs = self.api.recommendations(seed_tracks=track_ids)
        return RecommendedTracks.from_dict(songs).tracks

    def top_songs(self, id: str) -> list[Track]:
        songs = self.api.artist_top_tracks(id)
        return Tracks.from_dict(songs).tracks

    @combine_chunks
    def songs(self, ids: list[str]) -> list[Track]:
        songs = self.api.tracks(ids)
        return Tracks.from_dict(songs).tracks

    def albums(self, artist_id: str, album_type: str, amount: int) -> list[Album]:
        return self._albums(amount, artist_id, album_type)

    @combine_offsets
    def _albums(
        self, artist_id: str, album_type: str, limit: int, offset: int
    ) -> list[Album]:
        albums = self.api.artist_albums(
            artist_id, limit=limit, offset=offset, album_type=album_type
        )
        return Albums.from_dict(albums).items

    def album_songs(self, album: Album) -> list[AlbumTrack]:
        return self._album_songs(album.total_tracks, album.id)

    @combine_offsets
    def _album_songs(self, id_: str, offset: int, limit: int) -> list[AlbumTrack]:
        songs = self.api.album_tracks(id_, limit=limit, offset=offset)
        return AlbumTracks.from_dict(songs).items

    def album_count(self, artist_id: str, album_type: str = "album,single") -> int:
        albums = self.api.artist_albums(artist_id, limit=1, album_type=album_type)
        return Albums.from_dict(albums).total
