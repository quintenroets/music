from collections.abc import Iterator
from unittest.mock import MagicMock, patch

import pytest
from music.context import Context
from music.main import main
from music.models import Path
from music.models.response_types import Track


@pytest.fixture()
def _add_songs_context(context: Context, track: Track) -> Iterator[None]:
    context.options.add = track.full_name
    yield
    context.options.add = None


@patch("music.updaters.tracks.add_tracks_by_name")
@patch("music.main._main.collect_new_songs")
@pytest.mark.usefixtures("_add_songs_context")
def test_add_new_songs(
    add_tracks_by_name: MagicMock,
    collect_new_songs: MagicMock,
) -> None:
    main()
    methods = add_tracks_by_name, collect_new_songs
    for method in methods:
        method.assert_called_once()


@pytest.fixture()
def _clean_ids_context(context: Context) -> Iterator[None]:
    context.options.clean_download_ids = True
    yield
    context.options.clean_download_ids = False


@patch("music.updaters.download_ids.clean_download_ids")
@pytest.mark.usefixtures("_clean_ids_context")
def test_clean_ids_called(clean_download_ids: MagicMock) -> None:
    main()
    clean_download_ids.assert_called_once()


def fill_processed_songs() -> None:
    path = Path.processed_songs / "song.opus"
    path.touch()


@patch("music.main.uploader.start")
@patch(
    "music.download.download_new_songs.download_new_songs",
    side_effect=fill_processed_songs,
)
@pytest.mark.usefixtures("mocked_download_assets")
def test_main(upload: MagicMock, download: MagicMock) -> None:
    main()
    methods = upload, download
    for method in methods:
        method.assert_called_once()
