from music import storage
from music.models import Artist, ArtistType, Path


class Defaults:
    @classmethod
    def create_artists(cls) -> list[Artist]:
        return [
            Artist("4LLpKhyESsyAXpc4laK94U", "Mac Miller", ArtistType.FAVORITE),
            Artist("1VPmR4DJC1PlOtd0IADAO0", "$uicideboy$", ArtistType.NORMAL),
            Artist("2XnBwblw31dfGnspMIwgWz", "Axwell /\\ Ingrosso", ArtistType.NORMAL),
            Artist("6AgTAQt8XS6jRWi4sX7w49", "Polo G", ArtistType.NORMAL),
        ]

    @classmethod
    def create_downloaded_tracks(cls) -> dict[str, str]:
        return {
            "008q1ztvnmNxD7W4VjfHrm": "Mac Miller - Earth",
            "00Apys6jYrWA0Bse9Yon6O": "Bella Poarch, Lauv - Crush",
            "00Blm7zeNqgYLPtW6zg8cj": "Post Malone, The Weeknd - One Right Now",
        }

    @classmethod
    def create_tracks_to_download(cls) -> dict[str, str]:
        return {}


class Storage(storage.Storage):
    artists: list[Artist] = Path.artists.create_cached_content(
        default=Defaults.create_artists()
    )
    downloaded_tracks: dict[str, str] = Path.download_ids.create_cached_content(
        default=Defaults.create_downloaded_tracks()
    )
    tracks_to_download: dict[str, str] = Path.to_download.create_cached_content(
        default=Defaults.create_tracks_to_download()
    )

    def reset(self) -> None:
        self.artists = Defaults.create_artists()
        self.downloaded_tracks = Defaults.create_downloaded_tracks()
        self.tracks_to_download = Defaults.create_tracks_to_download()

    @property
    def artist_ids(self) -> list[str]:  # type: ignore[override]
        return [artist.id for artist in self.artists]
