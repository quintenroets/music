from __future__ import annotations

from dataclasses import dataclass

from .path import Path


@dataclass
class Config:
    frontend_port: int = 12000
    backend_port: int = 13000
    hostname: str = None

    def __post_init__(self):
        if self.hostname is None:
            self.hostname = f"http://localhost:{self.frontend_port}"

    @classmethod
    def load(cls):
        return cls(**Path.config.yaml)


config = Config.load()
