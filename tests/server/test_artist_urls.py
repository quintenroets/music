import pytest
from hypothesis import given, strategies

from music.runtime import Runtime
from music.server.routers.artists import parse_limit

from .client import RouteTestClient


@pytest.fixture(scope="session")
def client() -> RouteTestClient:
    return RouteTestClient("/artists")


def test_get(runtime: Runtime, client: RouteTestClient) -> None:
    params = {"limit": None}
    response = client.get_response("", params=params)
    artists = runtime.storage.artists
    assert len(artists) == len(response)
    for artist, artist_response in zip(artists, response, strict=False):
        assert artist.id == artist_response["id"]


@given(
    offset=strategies.integers(min_value=0, max_value=10),
    limit=strategies.integers(min_value=0, max_value=10),
)
def test_get_chunk(
    runtime: Runtime,
    client: RouteTestClient,
    offset: int,
    limit: int,
) -> None:
    params = {"limit": limit, "offset": offset}
    response = client.get_response("", params=params)
    artists = runtime.storage.artists[offset : offset + limit]
    assert len(artists) == len(response)
    for artist, artist_response in zip(artists, response, strict=False):
        assert artist.id == artist_response["id"]


def test_search(runtime: Runtime, client: RouteTestClient) -> None:
    artist = runtime.storage.artists[0]
    params = {"name": artist.name}
    response = client.get_response("search", params=params)
    assert response[0]["id"] == artist.id


def test_add(runtime: Runtime, client: RouteTestClient) -> None:
    artist = runtime.storage.artists.pop(0)
    assert artist.id not in runtime.storage.artist_ids
    params = {"name": artist.name, "id_": artist.id}
    client.get_response("add", params=params)
    assert artist.id in runtime.storage.artist_ids


def test_toggle(runtime: Runtime, client: RouteTestClient) -> None:
    artist = runtime.storage.artists[0]
    artist_type = artist.type_.value
    params = {"id_": artist.id}
    assert runtime.storage.get_artist(artist.id).type_.value == artist_type
    client.get_response("toggle", params=params)
    assert runtime.storage.get_artist(artist.id).type_.value != artist_type


def test_recommendations(runtime: Runtime, client: RouteTestClient) -> None:
    response = client.get_response("recommendations")
    assert isinstance(response, list)
    assert len(response) == runtime.context.config.number_of_recommendations


def test_parse_limit() -> None:
    parse_limit(None)
