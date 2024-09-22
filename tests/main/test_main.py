from collections.abc import Iterator
from unittest.mock import MagicMock, patch

import pytest

from music.context import Context
from music.main import main
from music.models import Path


@pytest.fixture
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
@pytest.mark.usefixtures("_mocked_download_assets")
def test_main(upload: MagicMock, download: MagicMock) -> None:
    main()
    methods = upload, download
    for method in methods:
        method.assert_called_once()
