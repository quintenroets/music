from collections.abc import Iterator

import pytest
from music.context import Context
from music.download import downloaded_songs_processor
from music.download.download_new_songs import download_new_songs
from music.models import Path


def test_downloader(context: Context, mocked_download_assets: None) -> None:
    path = Path.downloaded_songs / "song.opus"
    path.touch()
    context.storage.tracks_to_download = context.storage.downloaded_tracks
    download_new_songs()
    assert not path.exists()


def test_empty_file_detected(context: Context, mocked_download_assets: None) -> None:
    path = Path.downloaded_songs / "song.opus"
    path.touch()
    with pytest.raises(Exception, match=f"{path} is empty file"):
        downloaded_songs_processor.run()


@pytest.fixture
def notify_context(context: Context) -> Iterator[Context]:
    retries = context.config.download_retries
    context.config.download_retries = 0
    context.storage.tracks_to_download = context.storage.downloaded_tracks
    yield context
    context.config.download_retries = retries


def test_max_retries_notified(
    notify_context: Context, mocked_download_assets: None
) -> None:
    with pytest.raises(Exception, match="Max download retries reached"):
        download_new_songs()
