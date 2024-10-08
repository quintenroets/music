from unittest.mock import patch

import pytest
import spotipy

from music.clients.spotify import Client
from music.models.artist import Artist
from music.models.response_types import Track


@pytest.fixture
def track_ids(tracks: list[Track]) -> list[str]:
    return [track.id for track in tracks]


def test_search_artist(client: Client, artist: Artist) -> None:
    artists = client.search_artist(artist.name)
    assert any(artist.id == artist_result.id for artist_result in artists)


def test_artists(client: Client, artists: list[Artist]) -> None:
    ids = [artist.id for artist in artists]
    artists_result = client.artists(ids)
    for id_, artist_result in zip(ids, artists_result, strict=False):
        assert id_ == artist_result.id


def test_related_artists(client: Client, artist: Artist) -> None:
    client.related_artists(artist.id)


def test_top_songs(client: Client, artist: Artist) -> None:
    client.top_songs(artist.id)


def test_search_song(client: Client, track: Track) -> None:
    client.search_song(track.name)


def test_songs(client: Client, track_ids: list[str]) -> None:
    client.songs(track_ids)


def test_song_recommendations(client: Client, track_ids: list[str]) -> None:
    client.song_recommendations(track_ids[:1])


def test_albums(client: Client, artist: Artist) -> None:
    client.albums(artist.id, "single", 2)


def test_album_songs(client: Client, artist: Artist) -> None:
    album = client.albums(artist.id, "album", 1)[0]
    client.album_songs(album)


def test_album_count(client: Client, artist: Artist) -> None:
    client.album_count(artist.id)


def test_exception_handling(client: Client, track_ids: list[str]) -> None:
    exception = spotipy.exceptions.SpotifyException(None, None, None)
    patch_ = patch.object(spotipy.Spotify, "_internal_call", side_effect=exception)
    with patch_, pytest.raises(spotipy.exceptions.SpotifyException):
        client.song_recommendations(track_ids)
