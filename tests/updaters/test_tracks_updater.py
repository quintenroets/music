from collections.abc import Iterator
from unittest.mock import MagicMock, PropertyMock, patch

import pytest
from music import updaters
from music.context import context
from music.models import Path
from music.models.response_types import Track

track_names = ["Mac Miller - Earth", "Mac Miller - Best day ever"]


class MockStorage:
    @classmethod
    def save_new_tracks(cls, tracks: list[Track]) -> None:
        assert len(tracks) == len(track_names)


@pytest.fixture
def storage() -> Iterator[None]:
    mock_storage = PropertyMock(return_value=MockStorage())
    with patch.object(context, "storage", new_callable=mock_storage):
        mtime = Path.to_download.mtime
        yield
    assert Path.to_download.mtime == mtime


@patch("cli.confirm", return_value=True)
def test_tracks_confirmed(_: MagicMock, storage: None) -> None:
    updaters.tracks.add_tracks_by_name(track_names)


@patch.object(context, "storage")
@patch("cli.confirm", return_value=False)
def test_tracks_not_confirmed(_: MagicMock, storage: MagicMock) -> None:
    updaters.tracks.add_tracks_by_name(track_names)
    storage.assert_not_called()
