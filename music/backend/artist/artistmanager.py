from music.backend.client import spotapi
from music.backend.downloads import jobs
from music.backend.utils import Path

from .artist import FAVORITE, Artist


class ArtistPaths:
    def __init__(self, name):
        self.name = name.replace("/", "")

    @property
    def albums(self):
        path = Path.cache_assets / "albums" / self.name
        return path.with_suffix(".yaml")

    @property
    def album_count(self):
        path = Path.cache_assets / "album_counts" / self.name
        return path.with_suffix(".yaml")

    @property
    def top_songs(self):
        path = Path.cache_assets / "top_songs" / self.name
        return path.with_suffix(".yaml")


class ArtistManager(Artist):
    def __init__(self, artist):
        super().__init__(**artist.__dict__)
        self.path = ArtistPaths(self.name)

    @property
    def album_count(self):
        return self.path.album_count.yaml or 0

    def downloads(self):
        return self.path

    def collect_new_songs(self):
        if self.type == FAVORITE:
            self.check_all_songs()
        else:
            self.check_top_songs()

    def check_top_songs(self):
        cached_songs = self.path.top_songs.yaml
        songs = spotapi.top_songs(self.id)

        new_songs = [s for s in songs if s.id not in cached_songs]
        jobs.add(new_songs)

        new_songs_dict = {s.id: s.name for s in new_songs}
        self.path.top_songs.update(new_songs_dict)

    def check_all_songs(self):
        if spotapi.album_count(self.id) > self.album_count:
            albums = self.path.albums.yaml
            for album_type in ["album", "single"]:
                new_amount = spotapi.album_count(
                    self.id, album_type=album_type
                ) - albums.get(album_type, 0)

                if new_amount > 0:
                    new_albums = spotapi.albums(
                        self.id, album_type=album_type, amount=new_amount
                    )
                    for album in new_albums:
                        songs = spotapi.album_songs(album)
                        songs = spotapi.songs(
                            [song.id for song in songs]
                        )  # popularity and release_date needed
                        jobs.add(songs)
                        album_songs = {s.id: s.name for s in songs}
                        self.path.albums.update({album.id: album_songs})

                    self.path.album_count.yaml = self.album_count + len(new_albums)
