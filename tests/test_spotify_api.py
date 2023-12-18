from music.client import spotapi


def test_api() -> None:
    spotapi.search_artist("Mac Miller")
