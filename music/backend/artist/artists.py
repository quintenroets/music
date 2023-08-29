from ..utils import Path
from .artist import Artist

NORMAL = "normal"
FAVORITE = "favorite"


class Artists:
    def __init__(self):
        self.artists: dict[str, Artist] = {
            info["id"]: Artist(**info) for info in Path.artists.yaml
        }

    def __getitem__(self, item):
        return self.artists[item]

    def __setitem__(self, key, value):
        self.artists[key] = value

    def __iter__(self):
        yield from self.artist_list()

    def __len__(self):
        return len(self.artists)

    def artist_list(self):
        # use sort_index explicitely because dataclass ordering does not work
        return sorted(list(self.artists.values()), key=lambda a: a.sort_index)

    @property
    def ids(self):
        return [a.id for a in self.artist_list()]

    def add(self, artist):
        self[artist.id] = artist

    def save(self):
        Path.artists.yaml = [a.dict() for a in self.artist_list()]


artists = Artists()
