from dataclasses import dataclass
from functools import cached_property
from typing import Any

from package_utils.dataclasses.mixins import SerializationMixin

dataclass = dataclass(eq=False)  # type: ignore


@dataclass
class Urls:
    spotify: str


@dataclass
class IDS:
    isrc: str | None


@dataclass
class Item(SerializationMixin):
    external_urls: Urls
    href: str
    id: str
    name: str
    type: str
    uri: str

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass
class Followers:
    href: str | None
    total: int


@dataclass
class Image:
    height: int
    url: str
    width: int


@dataclass
class Artist(Item):
    pass


@dataclass
class ArtistInfo(Item):
    followers: Followers
    genres: list[str]
    images: list[Image]
    popularity: int


@dataclass
class Album(Item):
    album_type: str
    artists: list[Artist]
    images: list[Image]
    release_date: str
    release_date_precision: str
    total_tracks: int
    album_group: str | None
    is_playable: bool | None
    available_markets: list[str] | None
    restrictions: dict[str, str] | None


@dataclass
class AlbumTrack(Item):
    artists: list[Artist]
    disc_number: int
    duration_ms: int
    explicit: bool
    is_local: bool
    is_playable: bool | None
    preview_url: str | None
    track_number: int
    linked_from: dict[str, Any] | None
    restrictions: dict[str, str] | None


@dataclass
class Track(AlbumTrack):
    album: Album
    popularity: int
    external_ids: IDS
    available_markets: list[str] | None

    @property
    def should_download(self) -> bool:
        skip_names = ("Interlude", "Intro", "Outro", "Live", "Instrumental")
        return (
            2 * 60 * 1000 < self.duration_ms < 10 * 60 * 1000
            and self.popularity > 15
            and not any([f" - {skip_name}" in self.name for skip_name in skip_names])
        )

    @cached_property
    def full_name(self) -> str:
        artist_names = ", ".join(artist.name for artist in self.artists)
        name = f"{artist_names} - {self.name}"
        return name


@dataclass
class PaginatedResponse(SerializationMixin):
    href: str
    previous: str | None
    next: str | None
    limit: int
    offset: int
    total: int


@dataclass
class ArtistSearch(PaginatedResponse):
    items: list[ArtistInfo]


@dataclass
class Artists(SerializationMixin):
    artists: list[ArtistInfo]


@dataclass
class Tracks(SerializationMixin):
    tracks: list[Track]


@dataclass
class Albums(PaginatedResponse):
    items: list[Album]


@dataclass
class AlbumTracks(PaginatedResponse):
    items: list[AlbumTrack]


@dataclass
class TrackSearch(PaginatedResponse):
    items: list[Track]


@dataclass
class RecommendedTracks(Tracks):
    seeds: list[dict[str, str | int]]
