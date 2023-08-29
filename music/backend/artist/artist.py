from dataclasses import dataclass

NORMAL = "normal"
FAVORITE = "favorite"


@dataclass(order=True)
class Artist:
    id: str
    name: str
    type: str = NORMAL

    @property
    def sort_index(self):
        """Favorites first and then order by name."""
        return self.type == NORMAL, self.name

    def dict(self):
        return self.__dict__

    def toggle_type(self):
        self.type = FAVORITE if self.type == NORMAL else NORMAL
