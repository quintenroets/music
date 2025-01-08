import os
from dataclasses import dataclass, field


@dataclass
<<<<<<< HEAD
class Spotify:
    client_id: str
    client_secret: str
=======
class ApiSecrets:
    token: str = field(default_factory=lambda: os.environ.get("API_TOKEN", ""))
>>>>>>> template


@dataclass
class Secrets:
    genius_token: str
    spotify: Spotify
    phone_connection: str
