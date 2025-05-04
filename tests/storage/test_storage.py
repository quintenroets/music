from collections.abc import Iterator
from unittest.mock import PropertyMock, patch

import pytest

from music.models import Artist, Path
from music.models.response_types import Track
from music.runtime import Runtime
from music.storage import Storage


@pytest.fixture
def _mocked_artists_path() -> Iterator[None]:
    path = Path.tempfile()
    mocked_path = PropertyMock(return_value=path)
    mock = patch.object(Path, "artists", new_callable=mocked_path)
    with mock, path:
        yield


@pytest.mark.usefixtures("_mocked_artists_path")
def test_artists(runtime: Runtime, artists: list[Artist]) -> None:
    storage = Storage()
    artists = runtime.storage.artists
    storage.artists = artists
    assert storage.artists == artists
    new_artists = artists[1:]
    storage.artists = new_artists
    assert storage.artists == new_artists


def test_downloads(runtime: Runtime) -> None:
    downloads = runtime.storage.downloaded_tracks
    assert runtime.storage.downloaded_track_ids == set(downloads.keys())
    assert runtime.storage.downloaded_track_names == set(downloads.values())


def test_save_new_tracks(runtime: Runtime, track: Track) -> None:
    tracks = [track]
    runtime.storage.save_new_tracks(tracks)
    tracks_mapping = {track.id: track.full_name}
    assert runtime.storage.tracks_to_download == tracks_mapping
