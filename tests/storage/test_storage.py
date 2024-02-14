from unittest.mock import MagicMock, patch

from music.models import Artist
from music.models.response_types import IDS, Track
from music.storage import Storage

from ..updaters.test_artists_updater import album
from ..updaters.test_clean_download_ids import downloads


def test_artists(artists: list[Artist]) -> None:
    storage = Storage()
    assert storage.artists == artists
    new_artists = artists[1:]
    storage.artists = new_artists  # type: ignore
    assert storage.artists == new_artists


@patch("music.utils.cached_file_content.CachedFileContent.get")
def test_downloads(get: MagicMock) -> None:
    get.return_value = downloads
    storage = Storage()
    assert storage.downloaded_track_ids == set(downloads.keys())
    assert storage.downloaded_track_names == set(downloads.values())


@patch("music.utils.cached_file_content.CachedFileContent.get")
@patch("music.utils.cached_file_content.CachedFileContent.set")
def test_save_new_tracks(save: MagicMock, load: MagicMock) -> None:
    load.return_value = {}
    storage = Storage()
    track = Track(
        external_urls=album.external_urls,
        href="",
        id="id",
        name="name",
        type="",
        uri="",
        artists=[],
        disc_number=0,
        duration_ms=1000 * 60 * 3,
        explicit=True,
        is_local=True,
        is_playable=True,
        preview_url=None,
        track_number=0,
        linked_from=None,
        restrictions=None,
        album=album,
        popularity=100,
        external_ids=IDS(None),
        available_markets=None,
    )
    tracks = [track]
    storage.save_new_tracks(tracks)
    tracks_mapping = {track.id: track.full_name}
    save.assert_called_once_with(storage, tracks_mapping)  # yaml and json proxy
