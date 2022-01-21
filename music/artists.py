from .artist import Artist

NORMAL = 'normal'
FAVORITE = 'favorite'


class Artists:
    def __init__(self, artists):
        self._artists = artists

    @property
    def artists(self):
        return self._artists.values()

    @property
    def ids(self):
        return self._artists.keys()

    @classmethod
    def from_list(cls, info):
        artists = {i['id']: Artist.from_dict(i) for i in info}
        return cls(artists)

    def export(self):
        return [a.export() for a in sorted(self.artists, key=lambda a: a.name)]

    def get(self, id):
        return self._artists[id]

    def set(self, id, artist):
        self._artists[id] = artist

    def add(self, artist):
        self.set(artist.id, artist)

    def __iter__(self):
        yield from self.artists

    def __len__(self):
        return len(self._artists)