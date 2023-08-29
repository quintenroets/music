from music.backend.client import spotapi


def test_client():
    name = "Mac Miller"

    artists = spotapi.search_artist(name)

    ids = [a.id for a in artists]
    artists = spotapi.artists(ids)

    id = artists[0].id
    artists = spotapi.related_artists(id)

    id = artists[0].id
    songs = spotapi.top_songs(id)

    ids = [s.id for s in songs]
    songs = spotapi.songs(ids)

    album_count = spotapi.album_count(id)
    albums = spotapi.albums(id, "album,single", album_count)

    songs = spotapi.album_songs(albums[0])
