from music.models import Artist
from music.storage.artist import Storage


def test_artist_storage(artist: Artist) -> None:
    storage = Storage(artist)
    assert storage.albums_count is not None
    assert storage.album_counts is not None
    assert storage.top_tracks is not None
    assert storage.albums is not None
