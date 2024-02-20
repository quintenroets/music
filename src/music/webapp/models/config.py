from dataclasses import dataclass


@dataclass
class Config:
    app_name: str = "music.server:app"
    hostname: str = "https://music.com"
    frontend_repository: str = "quintenroets/music-frontend"
    backend_port: int = 13000
    session_name: str | None = None
