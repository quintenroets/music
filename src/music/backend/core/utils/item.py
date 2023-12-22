from dataclasses import dataclass
from typing import Any, TypeVar

import dacite

T = TypeVar("T")


@dataclass
class Item:
    @classmethod
    def from_dict(cls: type[T], items: dict[str, Any]) -> T:
        return dacite.from_dict(cls, items, config=dacite.Config(strict=True))  # type: ignore
