import pytest
from hypothesis import given, strategies

from music.context import Context

from .client import RouteTestClient


@pytest.fixture(scope="session")
def client() -> RouteTestClient:
    return RouteTestClient("/artists")


def test_get(context: Context, client: RouteTestClient) -> None:
    params = {"limit": None}
    response = client.get_response("", params=params)
    artists = context.storage.artists
    assert len(artists) == len(response)
    for artist, artist_response in zip(artists, response, strict=False):
        assert artist.id == artist_response["id"]


@given(
    offset=strategies.integers(min_value=0, max_value=10),
    limit=strategies.integers(min_value=0, max_value=10),
)
def test_get_chunk(
    context: Context, client: RouteTestClient, offset: int, limit: int
) -> None:
    params = {"limit": limit, "offset": offset}
    response = client.get_response("", params=params)
    artists = context.storage.artists[offset : offset + limit]
    assert len(artists) == len(response)
    for artist, artist_response in zip(artists, response, strict=False):
        assert artist.id == artist_response["id"]


def test_search(context: Context, client: RouteTestClient) -> None:
    artist = context.storage.artists[0]
    params = {"name": artist.name}
    response = client.get_response("search", params=params)
    assert response[0]["id"] == artist.id


def test_add(context: Context, client: RouteTestClient) -> None:
    artist = context.storage.artists.pop(0)
    assert artist.id not in context.storage.artist_ids
    params = {"name": artist.name, "id_": artist.id}
    client.get_response("add", params=params)
    assert artist.id in context.storage.artist_ids


def test_toggle(context: Context, client: RouteTestClient) -> None:
    artist = context.storage.artists[0]
    artist_type = artist.type_.value
    params = {"id_": artist.id}
    assert context.storage.get_artist(artist.id).type_.value == artist_type
    client.get_response("toggle", params=params)
    assert context.storage.get_artist(artist.id).type_.value != artist_type


def test_recommendations(context: Context, client: RouteTestClient) -> None:
    response = client.get_response("recommendations")
    assert isinstance(response, list)
    assert len(response) == context.config.number_of_recommendations
