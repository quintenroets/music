from collections.abc import Iterator
from unittest.mock import PropertyMock, patch

import pytest
from music import updaters
from music.context import context
from music.models import Path

downloads = {
    "008q1ztvnmNxD7W4VjfHrm": "Mac Miller - Earth",
    "00Apys6jYrWA0Bse9Yon6O": "Bella Poarch, Lauv - Crush",
    "00Blm7zeNqgYLPtW6zg8cj": "Post Malone, The Weeknd - One Right Now",
}


class MockStorage:
    @property
    def downloaded_tracks(self) -> dict[str, str]:
        return downloads

    @downloaded_tracks.setter
    def downloaded_tracks(self, tracks: dict[str, str]) -> None:
        names = set(downloads.values())
        for new_name in tracks.values():
            assert new_name in names


@pytest.fixture
def storage() -> Iterator[None]:
    mock_storage = PropertyMock(return_value=MockStorage())
    with patch.object(context, "storage", new_callable=mock_storage):
        mtime = Path.download_ids.mtime
        yield
    assert Path.download_ids.mtime == mtime


def test_clean_download_ids(storage: None) -> None:
    updaters.download_ids.clean_download_ids()
