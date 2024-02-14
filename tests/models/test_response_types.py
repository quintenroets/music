from collections.abc import Iterator

import pytest
from music.models.response_types import IDS, Album, Track, Urls


@pytest.fixture
def track() -> Iterator[Track]:
    duration_ms = 5 * 60 * 1000
    external_urls = Urls(spotify="")
    album = Album(
        external_urls=external_urls,
        href="",
        id="",
        name="",
        type="",
        uri="",
        album_type="",
        artists=[],
        images=[],
        release_date="",
        release_date_precision="",
        total_tracks=0,
        album_group=None,
        is_playable=None,
        available_markets=None,
        restrictions=None,
    )
    external_ids = IDS(isrc=None)
    track = Track(
        external_urls=external_urls,
        href="",
        id="",
        name="",
        type="",
        uri="",
        artists=[],
        disc_number=0,
        duration_ms=duration_ms,
        explicit=True,
        is_local=True,
        is_playable=True,
        preview_url=None,
        track_number=0,
        linked_from=None,
        restrictions=None,
        album=album,
        popularity=100,
        external_ids=external_ids,
        available_markets=None,
    )
    yield track


def test_should_download(track: Track) -> None:
    assert track.should_download is True


def test_hash(track: Track) -> None:
    assert hash(track) == hash(track.id)
