from . import _client
from .response_types import (
    Albums,
    AlbumTracks,
    Artists,
    ArtistSearch,
    RecommendedTracks,
    Tracks,
    TrackSearch,
)


def combine_chunks(f):
    """Combine function calls on chunks instead of whole array in one time
    :return: All results of the chunks.
    """

    def chunked_wrapper(*args, **kwargs):
        self, items, *args = args

        @combine_offsets
        def calculate_chunk(self, offset, limit):
            return f(self, items[offset : offset + limit], *args, **kwargs)

        return calculate_chunk(self, len(items))

    return chunked_wrapper


def combine_offsets(f, chunk_size=50):
    """Combine function calls with offset and limit instead of total amount
    :param chunk_size: Size of the chunks :return: All results of the
    chunks.
    """

    def chunked_wrapper(self, amount, *args, **kwargs):
        return [
            item
            for offset in range(0, amount, chunk_size)
            for item in f(self, *args, offset=offset, limit=chunk_size, **kwargs)
        ]

    return chunked_wrapper


class SpotApi:
    def __init__(self):
        self.api = _client.Spotify()

    def search_song(self, name):
        songs = self.api.search(name, type="track")
        return TrackSearch.from_dict(songs["tracks"]).items

    def search_artist(self, name):
        artists = self.api.search(name, type="artist")
        return ArtistSearch.from_dict(artists["artists"]).items

    @combine_chunks
    def artists(self, ids):
        artists = self.api.artists(ids)
        return Artists.from_dict(artists).artists

    def related_artists(self, id):
        artists = self.api.artist_related_artists(id)
        return Artists.from_dict(artists).artists

    def song_recommendations(self, track_ids):
        songs = self.api.recommendations(seed_tracks=track_ids)
        return RecommendedTracks.from_dict(songs).tracks

    def top_songs(self, id):
        songs = self.api.artist_top_tracks(id)
        return Tracks.from_dict(songs).tracks

    @combine_chunks
    def songs(self, ids):
        songs = self.api.tracks(ids)
        return Tracks.from_dict(songs).tracks

    def albums(self, artist_id, album_type, amount):
        return self._albums(amount, artist_id, album_type)

    @combine_offsets
    def _albums(self, artist_id, album_type, limit, offset):
        albums = self.api.artist_albums(
            artist_id, limit=limit, offset=offset, album_type=album_type
        )
        return Albums.from_dict(albums).items

    def album_songs(self, album):
        return self._album_songs(album.total_tracks, album.id)

    @combine_offsets
    def _album_songs(self, id_, offset, limit):
        songs = self.api.album_tracks(id_, limit=limit, offset=offset)
        return AlbumTracks.from_dict(songs).items

    def album_count(self, artist_id, album_type="album,single"):
        albums = self.api.artist_albums(artist_id, limit=1, album_type=album_type)
        return Albums.from_dict(albums).total
