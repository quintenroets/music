from dataclasses import dataclass

from ..context import context
from ..models import Artist
from ..models.response_types import Album
from ..storage.artist import Storage


@dataclass
class ArtistUpdater:
    artist: Artist

    def __post_init__(self) -> None:
        self.storage = Storage(self.artist)

    def check_for_new_songs(self) -> None:
        if self.artist.is_normal:
            self.check_top_songs()
        else:
            self.check_all_songs()

    def check_top_songs(self) -> None:
        tracks = context.spotify_client.top_songs(self.artist.id)
        new_tracks = [
            track for track in tracks if track.id not in self.storage.top_tracks
        ]
        context.storage.save_new_tracks(new_tracks)
        new_tracks_dict = {track.id: track.name for track in tracks}
        if new_tracks_dict:
            self.storage.top_tracks |= new_tracks_dict

    def check_all_songs(self) -> None:
        song_count = context.spotify_client.album_count(self.artist.id)
        if song_count > self.storage.albums_count:
            album_types = ("album", "single")
            for album_type in album_types:
                self.check_albums(album_type)
            self.storage.albums_count = song_count

    def check_albums(self, album_type: str) -> None:
        current_amount = context.spotify_client.album_count(
            self.artist.id, album_type=album_type
        )
        saved_amount = self.storage.get_album_count(album_type)
        added_amount = current_amount - saved_amount
        if added_amount > 0:
            self.save_new_albums(album_type, added_amount)

    def save_new_albums(self, album_type: str, amount: int) -> None:
        new_albums = context.spotify_client.albums(
            self.artist.id, album_type=album_type, amount=amount
        )
        for album in new_albums:
            self.save_new_album(album)
        num_new_albums = len(new_albums)
        self.storage.add_album_count(album_type, num_new_albums)

    def save_new_album(self, album: Album) -> None:
        tracks = context.spotify_client.album_songs(album)
        track_ids = [track.id for track in tracks]
        # popularity and release_date needed
        tracks_info = context.spotify_client.songs(track_ids)
        context.storage.save_new_tracks(tracks_info)
        album_tracks = {track.id: track.name for track in tracks_info}
        self.storage.albums |= {album.id: album_tracks}
