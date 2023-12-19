from __future__ import annotations

import os
from dataclasses import dataclass, field

from .item import Item
from .path import Path


@dataclass
class SpotifyTokens(Item):
    client_id: str = field(default_factory=lambda: os.environ["SPOTIFY_CLIENT_ID"])
    client_secret: str = field(
        default_factory=lambda: os.environ["SPOTIFY_CLIENT_SECRET"]
    )


@dataclass
class Tokens(Item):
    genius: str = field(default_factory=lambda: os.environ["GENIUS_TOKEN"])
    spotify: SpotifyTokens = field(default_factory=lambda: SpotifyTokens())

    @classmethod
    def load(cls) -> Tokens:
        items = Path.tokens.json
        return cls.from_dict(items)


tokens = Tokens.load()
