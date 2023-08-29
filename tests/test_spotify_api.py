from music.backend.client import spotapi


def test_api():
    spotapi.search_artist("Mac Miller")
