from dataclasses import asdict, dataclass
from typing import List, Optional

import dacite

dataclass = dataclass(eq=False)


@dataclass
class Urls:
    spotify: str


@dataclass
class IDS:
    isrc: Optional[str]


@dataclass
class Item:
    external_urls: Urls
    href: str
    id: str
    name: str
    type: str
    uri: str

    def __hash__(self):
        return hash(self.id)

    def dict(self):
        return asdict(self)


@dataclass
class Followers:
    href: Optional[str]
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
    genres: List[str]
    images: List[Image]
    popularity: int


@dataclass
class Album(Item):
    album_group: Optional[str]
    album_type: str
    artists: List[Artist]
    images: List[Image]
    release_date: str
    release_date_precision: str
    total_tracks: int


@dataclass
class AlbumTrack(Item):
    artists: List[Artist]
    disc_number: int
    duration_ms: int
    explicit: bool
    is_local: bool
    is_playable: bool
    preview_url: Optional[str]
    track_number: int
    linked_from: Optional[dict]
    restrictions: Optional[dict]


@dataclass
class Track(AlbumTrack):
    album: Album
    popularity: int
    external_ids: IDS


@dataclass
class Response:
    @classmethod
    def from_dict(cls, items):
        return dacite.from_dict(cls, items, config=dacite.Config(strict=True))


@dataclass
class PaginatedResponse(Response):
    href: str
    previous: Optional[str]
    next: Optional[str]
    limit: int
    offset: int
    total: int


@dataclass
class ArtistSearch(PaginatedResponse):
    items: List[ArtistInfo]


@dataclass
class Artists(Response):
    artists: List[ArtistInfo]


@dataclass
class Tracks(Response):
    tracks: List[Track]


@dataclass
class Albums(PaginatedResponse):
    items: List[Album]


@dataclass
class AlbumTracks(PaginatedResponse):
    items: List[AlbumTrack]


@dataclass
class TrackSearch(PaginatedResponse):
    items: List[Track]
