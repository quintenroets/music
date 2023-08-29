from __future__ import annotations

from dataclasses import dataclass

from .path import Path


@dataclass
class Config:
    backend_port: int = 13000
    hostname: str = None

    @classmethod
    def load(cls):
        return cls(**Path.config.yaml)


config = Config.load()
