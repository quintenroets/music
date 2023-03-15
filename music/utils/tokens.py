from dataclasses import dataclass

from .item import Item
from .path import Path


@dataclass
class SpotifyTokens(Item):
    client_id: str
    client_secret: str


@dataclass
class Tokens(Item):
    genius: str
    spotify: SpotifyTokens

    @classmethod
    def load(cls):
        items = Path.tokens.json
        return cls.from_dict(items)


tokens = Tokens.load()
