from dataclasses import dataclass

from .item import Item
from .path import Path


@dataclass
class SpotifyTokens:
    client_id: str
    client_secret: str

    @classmethod
    def from_dict(cls, info: dict):
        return SpotifyTokens(**info)


@dataclass
class Tokens(Item):
    genius: str
    spotify: SpotifyTokens

    @classmethod
    def load(cls):
        items = Path.tokens.json
        return cls.from_dict(items)


tokens = Tokens.load()
