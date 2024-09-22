from collections.abc import Iterator
from unittest.mock import MagicMock, patch

import pytest
from spotdl.types.song import Song

from music.context import Context
from music.download import downloaded_songs_processor
from music.download.download_new_songs import download_new_songs
from music.models import Path

download_songs = "spotdl.download.downloader.Downloader.download_multiple_songs"


def mock_download(songs: list[Song]) -> None:
    for song in songs:
        path = (Path.downloaded_songs / song.name).with_suffix(".opus")
        path.byte_content = b" "


@patch(download_songs, side_effect=mock_download)
@patch("mutagen.oggopus.OggOpus")
@pytest.mark.usefixtures("_mocked_download_assets")
def test_downloader(
    mocked_oggopus: MagicMock,
    mocked_download: MagicMock,
    context: Context,
) -> None:
    path = Path.downloaded_songs / "song.opus"
    path.touch()
    context.storage.tracks_to_download = context.storage.downloaded_tracks
    number_of_songs_to_download = len(context.storage.tracks_to_download)
    mocked_metadata = {"date": ["2000"], "title": [""]}
    mocked_oggopus.return_value.__getitem__ = lambda _, name: mocked_metadata[name]
    download_new_songs()
    mocked_download.assert_called_once()
    assert not path.exists()
    assert sum(1 for _ in Path.processed_songs.iterdir()) == number_of_songs_to_download


@patch("cli.run")
def test_youtube_downloader(mocked_run: MagicMock, context: Context) -> None:
    context.storage.youtube_tracks_to_download = ["mock_id"]
    download_new_songs()
    mocked_run.assert_called_once()


@pytest.mark.usefixtures("context", "_mocked_download_assets")
def test_empty_file_detected() -> None:
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


@pytest.mark.usefixtures("_mocked_download_assets")
@pytest.mark.usefixtures("notify_context")
def test_max_retries_notified() -> None:
    with pytest.raises(RuntimeError, match="Max download retries reached"):
        download_new_songs()
