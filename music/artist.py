from .path import Path

NORMAL = 'normal'
FAVORITE = 'favorite'


class Artist:
    def __init__(self, name, id, type=NORMAL):
        self.name = name
        self.id = id
        self.type = type

    def export(self):
        return self.__dict__

    def change_type(self):
        self.type = NORMAL if self.type == FAVORITE else FAVORITE

    @property
    def album_path(self):
        return Path.albums(self.name)

    @property
    def albums(self):
        return self.album_path.content

    @albums.setter
    def albums(self, albums):
        self.album_path.content = albums

    @classmethod
    def from_dict(cls, info):
        return cls(**info)