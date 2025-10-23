from typing import cast

import pytest

from music.runtime import Runtime
from tests.models.test_response_types import Track

from .client import RouteTestClient


@pytest.fixture(scope="session")
def client() -> RouteTestClient:
    return RouteTestClient("/songs")


def test_search(client: RouteTestClient, track: Track) -> None:
    params = {"name": track.name}
    response = client.get_response("search", params=params)
    assert isinstance(response, list)
    assert len(response) > 0
    assert "id" in response[0]


@pytest.mark.skip
def test_search_youtube(client: RouteTestClient, track: Track) -> None:
    response = search_youtube(client, track)
    assert isinstance(response, list)
    assert len(response) > 0
    assert "id" in response[0]


@pytest.mark.skip
def test_search_youtube_with_url(client: RouteTestClient, track: Track) -> None:
    response = search_youtube(client, track)
    id_ = response[0]["id"]
    track.name = f"https://www.youtube.com/watch?v={id_}"
    response = search_youtube(client, track)
    assert isinstance(response, list)
    assert len(response) == 1
    assert "id" in response[0]


def search_youtube(client: RouteTestClient, track: Track) -> list[dict[str, str]]:
    params = {"name": track.name}
    response = client.get_response("search/youtube", params=params)
    return cast("list[dict[str, str]]", response)


def test_add(runtime: Runtime, client: RouteTestClient, track: Track) -> None:
    assert track.id not in runtime.storage.tracks_to_download
    params = {"id_": track.id}
    client.get_response("add", params=params)
    assert track.id in runtime.storage.tracks_to_download


def test_add_youtube(runtime: Runtime, client: RouteTestClient, track: Track) -> None:
    params = {"id_": track.id, "youtube": True}
    client.get_response("add", params=params)
    assert track.id in runtime.storage.youtube_tracks_to_download


def test_recommendations(
    runtime: Runtime,
    client: RouteTestClient,
    tracks: list[Track],
) -> None:
    runtime.storage.downloaded_tracks = {track.id: "" for track in tracks}
    response = client.get_response("recommendations")
    assert isinstance(response, list)
    assert len(response) > 0
