from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from .path import Path

TIMEOUT = 1  # 3.05
RETRIES = 3 * 200  # 3 per artist

load_dotenv(dotenv_path=Path.env)

ccm = SpotifyClientCredentials(
    client_id=os.environ["SPOTAPI_ID"],
    client_secret=os.environ["SPOTAPI_SECRET"]
    )
sp = spotipy.Spotify(
    client_credentials_manager=ccm, requests_timeout=TIMEOUT, status_retries=0,
    retries=RETRIES, backoff_factor=1
)
MARKET = "BE"

# check if release date can be removed from top tracks (extra request that can be left out if release date not needed)

class SpotApi:
    @staticmethod
    def search(query, type_):
        return sp.search(query, type=type_)[type_ + "s"]["items"]

    @staticmethod
    def get_artists(name):
        return SpotApi.search(name, "artist")

    @staticmethod
    def get_recommended_artists(artist_id):
        return sp.artist_related_artists(artist_id)["artists"]

    @staticmethod
    def get_album_songs(album, chunck_size=50):
        amount = album["total_tracks"]
        id_ = album["id"]

        songs = [
            song
            for offset in range(0, amount, chunck_size)
            for song in sp.album_tracks(id_, limit=chunck_size, offset=offset, market=MARKET)["items"]
        ]
        for song in songs:
            song["release_date"] = album["release_date"]

        return songs

    @staticmethod
    def get_albums_amount(artist_id, album_type=None):
        if album_type is None:
            album_type = "album,single"
        return sp.artist_albums(artist_id, limit=1, album_type=album_type, country=MARKET)["total"]

    @staticmethod
    def get_albums(artist_id, album_type, amount, chunck_size=50):
        albums = [
            album
            for offset in range(0, amount, chunck_size)
            for album in sp.artist_albums(
                artist_id, limit=chunck_size, offset=offset, album_type=album_type, country=MARKET
            )["items"]
        ]

        albums = SpotApi.sort_unique(albums)
        return albums

    @staticmethod
    def get_top_songs(artist_id):
        songs = sp.artist_top_tracks(artist_id)["tracks"]
        for song in songs:
            song["release_date"] = song["album"]["release_date"]

        return songs

    @staticmethod
    def get_popularities(songs, chunck_size=50):
        song_ids = [song["id"] for song in songs]

        popularities = [
            pop
            for i in range(0, len(song_ids), chunck_size)
            for pop in sp.tracks(song_ids[i: i + chunck_size])["tracks"]
        ]
        return popularities

    @staticmethod
    def filter_song(song):
        skip_names = ["Interlude", "Intro", "Outro", "Live", "Instrumental"]
        skip = (
            int(song["duration_ms"]) < 2 * 60 * 1000
            or int(song["duration_ms"]) > 10 * 60 * 1000
            or any([f" - {skip_name}" in song["name"] for skip_name in skip_names])
        )
        return not skip

    @staticmethod
    def sort_unique(items):
        sorted_items = sorted(items, key=lambda item: item["release_date"], reverse=True) # first sort from new to old
        unique_items = list({item["name"]: item for item in items}.values()) # Unique by name and choose oldest if duplicates
        return unique_items

    @staticmethod
    def get_artist_infos(artists, chunck_size=50):
        ids = [a["id"] for a in artists]

        artists = [
            artist
            for i in range(0, len(ids), chunck_size)
            for artist in sp.artists(ids[i: i + chunck_size])["artists"]
        ]

        return artists
