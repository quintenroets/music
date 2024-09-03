from collections.abc import Iterator
from unittest.mock import PropertyMock, patch

import pytest

from music.context import Context
from music.models import Artist, Path
from music.models.response_types import Track
from music.storage import Storage


@pytest.fixture
def _mocked_artists_path() -> Iterator[None]:
    path = Path.tempfile()
    mocked_path = PropertyMock(return_value=path)
    mock = patch.object(Path, "artists", new_callable=mocked_path)
    with mock, path:
        yield


@pytest.mark.usefixtures("_mocked_artists_path")
def test_artists(context: Context, artists: list[Artist]) -> None:
    storage = Storage()
    artists = context.storage.artists
    storage.artists = artists
    assert storage.artists == artists
    new_artists = artists[1:]
    storage.artists = new_artists
    assert storage.artists == new_artists


def test_downloads(context: Context) -> None:
    downloads = context.storage.downloaded_tracks
    assert context.storage.downloaded_track_ids == set(downloads.keys())
    assert context.storage.downloaded_track_names == set(downloads.values())


def test_save_new_tracks(context: Context, track: Track) -> None:
    tracks = [track]
    context.storage.save_new_tracks(tracks)
    tracks_mapping = {track.id: track.full_name}
    assert context.storage.tracks_to_download == tracks_mapping
