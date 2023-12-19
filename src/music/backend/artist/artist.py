from dataclasses import dataclass

NORMAL = "normal"
FAVORITE = "favorite"


@dataclass(order=True)
class Artist:
    id: str
    name: str
    type: str = NORMAL

    @property
    def sort_index(self) -> tuple[bool, str]:
        """
        Favorites first and then order by name.
        """
        return self.type == NORMAL, self.name

    def dict(self) -> dict[str, str]:
        return self.__dict__

    def toggle_type(self) -> None:
        self.type = FAVORITE if self.type == NORMAL else NORMAL
