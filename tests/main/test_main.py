"""From collections.abc import Iterator from unittest.mock import MagicMock, patch.

import pytest
from music.context import Context, context
from music.main.main import main


@pytest.fixture
def test_download_songs_context() -> Iterator[None]:
    context.options.add = "Mac Miller - Earth"
    yield


@pytest.fixture
def test_clean_ids_context() -> Iterator[None]:
    context.options.clean_download_ids = True
    yield
    context.options.clean_download_ids = True


@patch("music.updaters.tracks.add_tracks_by_name")
@patch("music.download.download_new_songs")
def test_download_new_songs(
    add_tracks_by_name: MagicMock,
    download_new_songs: MagicMock,
    test_download_songs_context: Context,
) -> None:
    main()
    methods = add_tracks_by_name, download_new_songs
    for method in methods:
        method.assert_called_once()


@patch("music.updaters.download_ids.clean_download_ids")
def test_clean_ids_called(
    clean_download_ids: MagicMock, test_clean_ids_context: Context
) -> None:
    main()
    clean_download_ids.assert_called_once()
"""


def todo() -> None:
    pass
