from music.models.response_types import Track


def test_should_download(track: Track) -> None:
    track.duration_ms = 5 * 60 * 1000
    track.popularity = 100
    assert track.should_download is True


def test_hash(track: Track) -> None:
    assert hash(track) == hash(track.id)
