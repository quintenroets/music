from dataclasses import dataclass


@dataclass
class Spotify:
    client_id: str
    client_secret: str


@dataclass
class Secrets:
    genius_token: str
    spotify: Spotify
    phone_connection: str
