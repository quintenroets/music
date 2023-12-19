from music.backend.artist import ArtistManager
from music.backend.artist.artists import Artist


def test_artist() -> None:
    a = Artist("Famous", "id")
    a = ArtistManager(a)
    assert isinstance(a.dict(), dict)

    albums = {"album": 1}
    a.path.albums.yaml = albums
    assert a.path.albums.yaml == albums

    a.path.albums.unlink()
