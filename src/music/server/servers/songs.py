import random
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from music.models.response_types import Track
from music.models.youtube import Response
from music.runtime import runtime

if TYPE_CHECKING:
    from spotdl.types.result import Result  # pragma: nocover


@dataclass
class Server:
    number_of_song_recommendation_seeds: int = 5

    @classmethod
    def create_song_search_results(cls, name: str) -> Iterator[dict[str, Any]]:
        songs = runtime.spotify_client.search_song(name)
        for song, is_downloaded in cls.check_is_downloaded(songs):
            yield song.dict() | {"downloaded": is_downloaded}

    @classmethod
    def check_is_downloaded(
        cls,
        songs: Iterable[Track],
    ) -> Iterator[tuple[Track, bool]]:
        downloaded_tracks = runtime.storage.downloaded_tracks
        downloaded_track_names = set(downloaded_tracks.values())
        for song in songs:
            is_downloaded = (
                song.id in downloaded_tracks or song.full_name in downloaded_track_names
            )
            yield song, is_downloaded

    def create_song_recommendations(self) -> Iterator[Track]:
        downloaded_song_ids = list(runtime.storage.downloaded_tracks.keys())
        random.shuffle(downloaded_song_ids)
        seed_ids = downloaded_song_ids[: self.number_of_song_recommendation_seeds]
        recommendations = runtime.spotify_client.song_recommendations(seed_ids)
        for song, is_downloaded in self.check_is_downloaded(recommendations):
            if not is_downloaded:
                yield song

    @classmethod
    def create_youtube_search_results(cls, name: str) -> Iterator[dict[str, Any]]:
        if "youtube" in name:
            results = cls.create_youtube_result(name)
        else:
            results = runtime.youtube_music_client.get_results(name)
        for result in results:
            yield Response.from_result(result).info

    @classmethod
    def create_youtube_result(cls, name: str) -> Iterator["Result"]:
        id_ = name.split("?v=")[-1]
        results = runtime.youtube_music_client.get_results(id_)
        for result in results:
            if result.result_id == id_:
                yield result
