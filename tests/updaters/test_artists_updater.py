from collections.abc import Iterator
from dataclasses import dataclass
from unittest.mock import PropertyMock, patch

import pytest
from music.context import context
from music.models import Artist, Path
from music.models.response_types import (
    Album,
    Image,
    Track,
    Urls,
)
from music.models.response_types import (
    Artist as ArtistResponse,
)
from music.updaters import artists as artists_updater

response_artists = [
    ArtistResponse(
        external_urls=Urls(
            spotify="https://open.spotify.com/artist/4LLpKhyESsyAXpc4laK94U"
        ),
        href="https://api.spotify.com/v1/artists/4LLpKhyESsyAXpc4laK94U",
        id="4LLpKhyESsyAXpc4laK94U",
        name="Mac Miller",
        type="artist",
        uri="spotify:artist:4LLpKhyESsyAXpc4laK94U",
    )
]
images = [
    Image(
        height=640,
        url="https://i.scdn.co/image/ab67616d0000b27388135807538061ab8c2c670f",
        width=640,
    ),
    Image(
        height=300,
        url="https://i.scdn.co/image/ab67616d00001e0288135807538061ab8c2c670f",
        width=300,
    ),
    Image(
        height=64,
        url="https://i.scdn.co/image/ab67616d0000485188135807538061ab8c2c670f",
        width=64,
    ),
]


album = Album(
    external_urls=Urls(spotify="https://open.spotify.com/album/0Wf65emw9eAwbjJ45gMMqp"),
    href="https://api.spotify.com/v1/albums/0Wf65emw9eAwbjJ45gMMqp",
    id="0Wf65emw9eAwbjJ45gMMqp",
    name="Watching Movies with the Sound Off (10th Anniversary)",
    type="album",
    uri="spotify:album:0Wf65emw9eAwbjJ45gMMqp",
    album_type="album",
    artists=response_artists,
    images=images,
    release_date="2023-06-23",
    release_date_precision="day",
    total_tracks=20,
    album_group="album",
    is_playable=True,
    available_markets=None,
    restrictions=None,
)


@dataclass
class MockStorage:
    artists: list[Artist]

    @classmethod
    def save_new_tracks(cls, tracks: list[Track]) -> None:
        pass


@pytest.fixture
def cache_assets_path() -> Iterator[None]:
    with Path.tempfile(create=False) as path:
        path.mkdir()
        mock_path = PropertyMock(return_value=path)
        with patch.object(Path, "cache_assets", new_callable=mock_path):
            yield


@pytest.fixture
def storage(artists: list[Artist]) -> Iterator[None]:
    mock_storage = PropertyMock(return_value=MockStorage(artists))
    with patch.object(context, "storage", new_callable=mock_storage):
        mtime = Path.artists.mtime
        yield
    assert Path.artists.mtime == mtime


def test_check_for_new_songs(storage: None, cache_assets_path: None) -> None:
    with patch("music.clients.spotify.Client.albums", return_value=[album]):
        artists_updater.check_for_new_songs()
    with patch("music.updaters.artist.ArtistUpdater.check_albums") as check_albums:
        artists_updater.check_for_new_songs()
        check_albums.assert_not_called()
