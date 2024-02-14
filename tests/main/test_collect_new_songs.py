"""From collections.abc import Iterator from unittest.mock import MagicMock,
PropertyMock, patch.

import pytest
from music.context import context
from music.main.main import collect_new_songs
from music.models import Path

track_names = ["Mac Miller - Earth", "Mac Miller - Best day ever"]


class MockStorage:
    @property
    def tracks_to_download(self) -> None:
        return None


@pytest.fixture
def storage() -> Iterator[None]:
    mock_storage = PropertyMock(return_value=MockStorage())
    with patch.object(context, "storage", new_callable=mock_storage):
        yield


@patch("music.download.download_new_songs")
@patch("music.updaters.artists.check_for_new_songs")
@patch.object(Path.processed_songs, "is_empty", return_value=True)
def test_collect_new_songs(
    _: MagicMock,
    check_for_new_songs: MagicMock,
    download_new_songs: MagicMock,
    storage: None,
) -> None:
    collect_new_songs()
    check_for_new_songs.assert_called_once()
    download_new_songs.assert_not_called()
"""


def todo() -> None:
    pass
