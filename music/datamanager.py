import spotipy
import requests
from retry import retry

from .artist import Artist
from .data import Data
from .path import Path
from .spotapi import SpotApi


class DataManager:
    @staticmethod
    def change_type(id):
        artists = Data.artists()
        artist = artists.get(id)
        artist.change_type()
        artists.set(id, artist)
        Data.save_artists(artists)

    @staticmethod
    def add_artist(artist):
        artist = Artist.from_dict(artist)
        artists = Data.artists()
        if artist.id not in artist.ids:
            artists.add(artist)
            Data.save_artists(artists)

    @staticmethod
    def get_new_artists(name):
        artist_ids = Data.artists().ids
        new_artists = SpotApi.get_artists(name)
        for a in new_artists:
            a["added"] = a["id"] in artist_ids
        return new_artists

    @staticmethod
    @retry(spotipy.exceptions.SpotifyException, delay=2)
    @retry(requests.exceptions.ReadTimeout)
    def get_new_songs(artist, all=False):
        songs = (
            DataManager.get_all_new_songs(artist)
            if all
            else SpotApi.get_top_songs(artist.id)
        )
        songs = [s for s in songs if int(s["popularity"]) > 15]
        songs = sorted(songs, key=lambda song: song["popularity"], reverse=True)
        return songs

    @staticmethod
    def get_all_new_songs(artist):
        albums = DataManager.get_new_albums(artist)

        songs = [
            song
            for album in albums
            for song in SpotApi.get_album_songs(album)
            if SpotApi.filter_song(song)
        ]

        songs = SpotApi.sort_unique(songs)
        popularities = SpotApi.get_popularities(songs)
        for s, p in zip(songs, popularities):
            s["popularity"] = p["popularity"]
        return songs

    @staticmethod
    def get_new_albums(artist, chunck_size=50):
        new_albums = []
        counts = artist.albums

        new_amount = SpotApi.get_albums_amount(artist.id)
        if new_amount > sum(counts.values()):

            for album_type in ["album", "single"]:
                extra_amount = SpotApi.get_albums_amount(
                    artist.id, album_type=album_type
                )
                counts[album_type] = counts.get(album_type, 0) + extra_amount
                new_albums += SpotApi.get_albums(artist.id, album_type, extra_amount)

            artist.albums = counts

        return new_albums

    @staticmethod
    def filter_downloads(songs):
        all_downloads = Path.downloads.load()
        songs = {id_: song for id_, song in songs.items() if id_ not in all_downloads}
        return songs

    @staticmethod
    def remove_new_songs(done):
        songs = Path.songs.load()
        for id_ in done:
            if id_ in songs:
                songs.pop(id_)
        Path.songs.save(songs)

    @staticmethod
    def add_new_songs(new_songs):
        new_songs = DataManager.filter_downloads(new_songs)

        songs = Path.songs.load()
        songs.update(new_songs)
        Path.songs.save(songs)

        all_downloads = Path.downloads.load()
        all_downloads.update(new_songs)
        Path.downloads.save(all_downloads)
