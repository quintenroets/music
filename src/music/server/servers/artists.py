import random
from collections.abc import Iterator
from itertools import islice
from typing import Any

from music.models.response_types import ArtistInfo
from music.runtime import runtime


class Server:
    @classmethod
    def create_artist_search_results(cls, name: str) -> Iterator[dict[str, Any]]:
        saved_artist_ids = runtime.storage.artist_ids
        artists = runtime.spotify_client.search_artist(name)
        for artist in artists:
            is_added = artist.id in saved_artist_ids
            yield artist.dict() | {"added": is_added}

    @classmethod
    def create_artist_recommendations(cls) -> list[ArtistInfo]:
        recommendations = cls._create_artist_recommendations()
        cls.increase_recommendation_frequencies(recommendations)
        frequencies = runtime.storage.recommendation_frequencies
        return sorted(recommendations, key=lambda artist: frequencies[artist.id])

    @classmethod
    def _create_artist_recommendations(cls) -> set[ArtistInfo]:
        iterator = cls.generate_recommended_artists()
        limited_iterator = islice(
            iterator,
            runtime.context.config.number_of_recommendations,
        )
        return set(limited_iterator)

    @classmethod
    def generate_recommended_artists(cls) -> Iterator[ArtistInfo]:
        saved_artist_ids = list(runtime.storage.artist_ids)
        random.shuffle(saved_artist_ids)
        seed_ids = saved_artist_ids[
            : runtime.context.config.max_new_recommendation_tries
        ]
        for id_ in seed_ids:
            related_artists = runtime.spotify_client.related_artists(id_)
            for artist in related_artists:
                if artist.id not in saved_artist_ids:
                    yield artist

    @classmethod
    def increase_recommendation_frequencies(cls, artists: set[ArtistInfo]) -> None:
        frequencies = runtime.storage.recommendation_frequencies
        for artist in artists:
            frequencies[artist.id] = frequencies.get(artist.id, 0) + 1
        runtime.storage.recommendation_frequencies = frequencies

    @classmethod
    def load_saved_artists(
        cls,
        offset: int,
        limit: int | None,
    ) -> Iterator[dict[str, str]]:
        artists = runtime.storage.artists
        limited_artists = (
            artists[offset:] if limit is None else artists[offset : offset + limit]
        )
        ids = [artist.id for artist in limited_artists]
        api_infos = runtime.spotify_client.artists(ids)
        for artist, info in zip(limited_artists, api_infos, strict=False):
            yield info.dict() | artist.dict()
