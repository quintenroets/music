from ..models import Secrets
from ..models.response_types import (
    Album,
    Albums,
    AlbumTrack,
    AlbumTracks,
    ArtistInfo,
    Artists,
    ArtistSearch,
    RecommendedTracks,
    Track,
    Tracks,
    TrackSearch,
)
from . import _spotify
from .utils import combine_chunks, combine_offsets


class Client:
    def __init__(self, secrets: Secrets) -> None:
        self.client = _spotify.Spotify(secrets)

    def search_song(self, name: str) -> list[Track]:
        songs = self.client.search(name, type="track")
        return TrackSearch.from_dict(songs["tracks"]).items

    def search_artist(self, name: str) -> list[ArtistInfo]:
        artists = self.client.search(name, type="artist")
        return ArtistSearch.from_dict(artists["artists"]).items

    @combine_chunks
    def artists(self, ids: list[str]) -> list[ArtistInfo]:
        artists = self.client.artists(ids)
        return Artists.from_dict(artists).artists

    def related_artists(self, id: str) -> list[ArtistInfo]:
        artists = self.client.artist_related_artists(id)
        return Artists.from_dict(artists).artists

    def song_recommendations(self, track_ids: list[str]) -> list[Track]:
        songs = self.client.recommendations(seed_tracks=track_ids)
        return RecommendedTracks.from_dict(songs).tracks

    def top_songs(self, id: str) -> list[Track]:
        songs = self.client.artist_top_tracks(id)
        return Tracks.from_dict(songs).tracks

    @combine_chunks
    def songs(self, ids: list[str]) -> list[Track]:
        songs = self.client.tracks(ids)
        return Tracks.from_dict(songs).tracks

    def albums(self, artist_id: str, album_type: str, amount: int) -> list[Album]:
        return self._albums(amount, artist_id, album_type)

    @combine_offsets
    def _albums(
        self, artist_id: str, album_type: str, limit: int, offset: int
    ) -> list[Album]:
        albums = self.client.artist_albums(
            artist_id, limit=limit, offset=offset, album_type=album_type
        )
        return Albums.from_dict(albums).items

    def album_songs(self, album: Album) -> list[AlbumTrack]:
        return self._album_songs(album.total_tracks, album.id)

    @combine_offsets
    def _album_songs(self, id_: str, offset: int, limit: int) -> list[AlbumTrack]:
        songs = self.client.album_tracks(id_, limit=limit, offset=offset)
        return AlbumTracks.from_dict(songs).items

    def album_count(self, artist_id: str, album_type: str = "album,single") -> int:
        albums = self.client.artist_albums(artist_id, limit=1, album_type=album_type)
        return Albums.from_dict(albums).total
