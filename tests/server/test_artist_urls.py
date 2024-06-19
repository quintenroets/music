import pytest
from music.context import Context

from .client import RouteTestClient


@pytest.fixture
def client() -> RouteTestClient:
    return RouteTestClient("/artists")


def test_get(context: Context, client: RouteTestClient) -> None:
    response = client.get_response("")
    artists = context.storage.artists
    assert len(artists) == len(response)
    for artist, artist_response in zip(artists, response):
        assert artist.id == artist_response["id"]


def test_search(context: Context, client: RouteTestClient) -> None:
    artist = context.storage.artists[0]
    params = {"name": artist.name}
    response = client.get_response("search", params=params)
    assert response[0]["id"] == artist.id


def test_add(context: Context, client: RouteTestClient) -> None:
    artist = context.storage.artists.pop(0)
    assert artist.id not in context.storage.artist_ids
    params = {"name": artist.name, "id": artist.id}
    client.get_response("add", params=params)
    assert artist.id in context.storage.artist_ids


def test_toggle(context: Context, client: RouteTestClient) -> None:
    artist = context.storage.artists[0]
    artist_type = artist.type_.value
    params = {"id": artist.id}
    assert context.storage.get_artist(artist.id).type_.value == artist_type
    client.get_response("toggle", params=params)
    assert context.storage.get_artist(artist.id).type_.value != artist_type


def test_recommendations(context: Context, client: RouteTestClient) -> None:
    response = client.get_response("recommendations")
    assert isinstance(response, list)
    assert len(response) == context.config.number_of_recommendations
