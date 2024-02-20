from dataclasses import dataclass
from enum import Enum
from typing import Any

import dacite
from package_utils.dataclasses.mixins import SerializationMixin, T


class ArtistType(Enum):
    NORMAL = "normal"
    FAVORITE = "favorite"


@dataclass(order=True)
class Artist(SerializationMixin):
    id: str
    name: str
    type_: ArtistType = ArtistType.NORMAL

    @classmethod
    def from_dict(
        cls: type[T], items: dict[str, Any], config: dacite.Config | None = None
    ) -> T:
        config = dacite.Config(type_hooks={ArtistType: ArtistType})
        if "type" in items:
            items["type_"] = items.pop("type")
        return super().from_dict(items, config)

    def dict(self) -> dict[str, str]:
        items = super().dict()
        items["type"] = items.pop("type_").value
        return items

    @property
    def sort_index(self) -> tuple[bool, str]:
        """
        Favorites first and then order by name.
        """
        return self.is_normal, self.name

    def toggle_type(self) -> None:
        self.type_ = ArtistType.FAVORITE if self.is_normal else ArtistType.NORMAL

    @property
    def is_normal(self) -> bool:
        return self.type_ == ArtistType.NORMAL
