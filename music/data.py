from .path import Path
from .artists import Artists


class Data:
    @classmethod
    def artists(cls):
        return Artists.from_list(Path.artists.content)

    @classmethod
    def save_artists(cls, artists):
        Path.artists.content = artists.export()