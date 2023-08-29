from dataclasses import dataclass

import dacite


@dataclass
class Item:
    @classmethod
    def from_dict(cls, items):
        return dacite.from_dict(cls, items, config=dacite.Config(strict=True))
