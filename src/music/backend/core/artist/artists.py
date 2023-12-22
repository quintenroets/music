from collections.abc import Iterator

from ..utils import Path
from .artist import Artist

NORMAL = "normal"
FAVORITE = "favorite"


class Artists:
    def __init__(self) -> None:
        self.artists: dict[str, Artist] = {
            info["id"]: Artist(**info) for info in Path.artists.yaml
        }

    def __getitem__(self, item: str) -> Artist:
        return self.artists[item]

    def __setitem__(self, key: str, value: Artist) -> None:
        self.artists[key] = value

    def __iter__(self) -> Iterator[Artist]:
        yield from self.artist_list()

    def __len__(self) -> int:
        return len(self.artists)

    def artist_list(self) -> list[Artist]:
        # use sort_index explicitely because dataclass ordering does not work
        return sorted(list(self.artists.values()), key=lambda a: a.sort_index)

    @property
    def ids(self) -> list[str]:
        return [a.id for a in self.artist_list()]

    def add(self, artist: Artist) -> None:
        self[artist.id] = artist

    def save(self) -> None:
        Path.artists.yaml = [a.dict() for a in self.artist_list()]


artists = Artists()
