from music.artist import ArtistManager
from music.artist.artists import Artist


def test_artist():
    a = Artist("Famous", "id")
    a = ArtistManager(a)
    assert isinstance(a.dict(), dict)

    albums = {"album": 1}
    a.path.albums.content = albums
    assert a.path.albums.content == albums

    a.path.albums.unlink()


test_artist()
