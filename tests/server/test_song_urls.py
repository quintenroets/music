import pytest
from music.context import Context

from tests.models.test_response_types import Track

from .client import RouteTestClient


@pytest.fixture
def client() -> RouteTestClient:
    return RouteTestClient("/songs")


def test_search(client: RouteTestClient, track: Track) -> None:
    params = {"name": track.name}
    response = client.get_response("search", params=params)
    assert isinstance(response, list)
    assert len(response) > 1
    assert "id" in response[0]


def test_add(
    context: Context, mocked_storage: None, client: RouteTestClient, track: Track
) -> None:
    assert track.id not in context.storage.tracks_to_download
    params = {"id": track.id}
    client.get_response("add", params=params)
    assert track.id in context.storage.tracks_to_download


def test_recommendations(
    context: Context, mocked_storage: None, client: RouteTestClient, tracks: list[Track]
) -> None:
    context.storage.downloaded_tracks = {track.id: "" for track in tracks}
    response = client.get_response("recommendations")
    assert isinstance(response, list)
    assert len(response) > 0
