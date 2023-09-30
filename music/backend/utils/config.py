from __future__ import annotations

from dataclasses import dataclass

from .path import Path


@dataclass
class Config:
    hostname: str
    backend_port: int = 13000

    @classmethod
    def load(cls):
        return cls(**Path.config.yaml)


config = Config.load()
