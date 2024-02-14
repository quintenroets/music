import typing

from ..models import Artist, Path


class Paths:
    def __init__(self, artist: Artist) -> None:
        self.name = artist.name.replace("/", "")

    @property
    def albums(self) -> Path:
        return self.create_path("albums")

    @property
    def albums_count(self) -> Path:
        return self.create_path("albums_count")

    @property
    def album_counts(self) -> Path:
        return self.create_path("album_counts")

    @property
    def top_tracks(self) -> Path:
        return self.create_path("top_tracks")

    def create_path(self, name: str) -> Path:
        path = Path.cache_assets / name / self.name
        path = path.with_suffix(".yaml")
        return typing.cast(Path, path)
