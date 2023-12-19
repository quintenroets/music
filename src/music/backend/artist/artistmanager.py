from dataclasses import dataclass

from ..client import spotapi
from ..downloads import jobs
from ..utils import Path
from .artist import FAVORITE, Artist


@dataclass
class ArtistPaths:
    name: str

    def __post_init__(self) -> None:
        self.name = self.name.replace("/", "")

    @property
    def albums(self) -> Path:
        path = Path.cache_assets / "albums" / self.name
        return path.with_suffix(".yaml")  # type: ignore

    @property
    def album_count(self) -> Path:
        path = Path.cache_assets / "album_counts" / self.name
        return path.with_suffix(".yaml")  # type: ignore

    @property
    def top_songs(self) -> Path:
        path = Path.cache_assets / "top_songs" / self.name
        return path.with_suffix(".yaml")  # type: ignore


class ArtistManager(Artist):
    def __init__(self, artist: Artist) -> None:
        super().__init__(**artist.__dict__)
        self.path = ArtistPaths(self.name)

    @property
    def album_count(self) -> int:
        return self.path.album_count.yaml or 0  # type: ignore

    def downloads(self) -> ArtistPaths:
        return self.path

    def collect_new_songs(self) -> None:
        if self.type == FAVORITE:
            self.check_all_songs()
        else:
            self.check_top_songs()

    def check_top_songs(self) -> None:
        cached_songs = self.path.top_songs.yaml
        assert isinstance(cached_songs, dict)
        songs = spotapi.top_songs(self.id)

        new_songs = [s for s in songs if s.id not in cached_songs]
        jobs.add(new_songs)

        new_songs_dict = {s.id: s.name for s in new_songs}
        self.path.top_songs.update(new_songs_dict)

    def check_all_songs(self) -> None:
        if spotapi.album_count(self.id) > self.album_count:
            albums = self.path.albums.yaml
            assert isinstance(albums, dict)
            for album_type in ["album", "single"]:
                new_amount = spotapi.album_count(self.id, album_type=album_type)
                saved_amount = albums.get(album_type, 0)
                added_amount = new_amount - saved_amount

                if added_amount > 0:
                    new_albums = spotapi.albums(
                        self.id, album_type=album_type, amount=added_amount
                    )
                    for album in new_albums:
                        songs = spotapi.album_songs(album)
                        songs_info = spotapi.songs(
                            [song.id for song in songs]
                        )  # popularity and release_date needed
                        jobs.add(songs_info)
                        album_songs = {s.id: s.name for s in songs_info}
                        self.path.albums.update({album.id: album_songs})

                    self.path.album_count.yaml = self.album_count + len(new_albums)
