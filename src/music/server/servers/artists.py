import random
from collections.abc import Iterator
from dataclasses import dataclass
from itertools import islice
from typing import Any

from ...context import context
from ...models.response_types import ArtistInfo


@dataclass
class Server:
    number_of_recommendations: int = 50
    max_new_recommendation_tries: int = 10

    @classmethod
    def create_artist_search_results(cls, name: str) -> Iterator[dict[str, Any]]:
        saved_artist_ids = context.storage.artist_ids
        artists = context.spotify_client.search_artist(name)
        for artist in artists:
            is_added = artist.id in saved_artist_ids
            yield artist.dict() | {"added": is_added}

    def create_artist_recommendations(self) -> list[ArtistInfo]:
        recommendations = self._create_artist_recommendations()
        self.increase_recommendation_frequencies(recommendations)
        frequencies = context.storage.recommendation_frequencies
        return sorted(recommendations, key=lambda artist: frequencies[artist.id])

    def _create_artist_recommendations(self) -> set[ArtistInfo]:
        iterator = self.generate_recommended_artists()
        limited_iterator = islice(iterator, self.number_of_recommendations)
        return set(limited_iterator)

    def generate_recommended_artists(self) -> Iterator[ArtistInfo]:
        saved_artist_ids = list(context.storage.artist_ids)
        random.shuffle(saved_artist_ids)
        seed_ids = saved_artist_ids[: self.max_new_recommendation_tries]
        for id_ in seed_ids:
            related_artists = context.spotify_client.related_artists(id_)
            for artist in related_artists:
                if artist.id not in saved_artist_ids:
                    yield artist

    @classmethod
    def increase_recommendation_frequencies(cls, artists: set[ArtistInfo]) -> None:
        frequencies = context.storage.recommendation_frequencies
        for artist in artists:
            frequencies[artist.id] = frequencies.get(artist.id, 0) + 1
        context.storage.recommendation_frequencies = frequencies

    @classmethod
    def load_saved_artists(cls) -> Iterator[dict[str, str]]:
        artists = context.storage.artists
        artist_ids = list(context.storage.artist_ids)
        api_infos = context.spotify_client.artists(artist_ids)
        for artist, info in zip(artists, api_infos):
            yield info.dict() | artist.dict()
