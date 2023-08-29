from dataclasses import asdict, dataclass

from ..utils.item import Item as Response

dataclass = dataclass(eq=False)


@dataclass
class Urls:
    spotify: str


@dataclass
class IDS:
    isrc: str | None


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
    restrictions: dict | None


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
    linked_from: dict | None
    restrictions: dict | None


@dataclass
class Track(AlbumTrack):
    album: Album
    popularity: int
    external_ids: IDS
    available_markets: list[str] | None


@dataclass
class PaginatedResponse(Response):
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
class Artists(Response):
    artists: list[ArtistInfo]


@dataclass
class Tracks(Response):
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
    seeds: list[dict]
