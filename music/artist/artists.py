from music.path import Path

from .artist import Artist

NORMAL = "normal"
FAVORITE = "favorite"


class Artists:
    def __init__(self):
        self.artists = {info["id"]: Artist(**info) for info in Path.artists.content}

    def __getitem__(self, item):
        return self.artists[item]

    def __setitem__(self, key, value):
        self.artists[key] = value

    def __iter__(self):
        yield from self.artists.values()

    def __len__(self):
        return len(self.artists)

    @property
    def ids(self):
        return self.artists.keys()

    def export(self):
        return

    def add(self, artist):
        self[artist.id] = artist

    def save(self):
        Path.artists.content = [a.dict() for a in sorted(self.artists)]
