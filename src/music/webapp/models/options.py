from dataclasses import dataclass

from .path import Path


@dataclass
class Options:
    config_path: Path = Path.config
    headless: bool = False
    debug: bool = False
    restart: bool = False
    update_frontend: bool = False
    backend: bool = False
