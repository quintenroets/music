from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TypeVar

import dacite
import requests
from package_utils.dataclasses.mixins import SerializationMixin

from music.webapp.context import context

T = TypeVar("T")


@dataclass
class FrontendRelease(SerializationMixin):
    updated_at: str
    browser_download_url: str

    @classmethod
    def load(cls) -> FrontendRelease:
        release_url = f"https://api.github.com/repos/{context.config.frontend_repository}/releases/latest"
        frontend_info = requests.get(release_url).json()["assets"][0]
        config = dacite.Config(strict=False)
        return cls.from_dict(frontend_info, config=config)

    @property
    def mtime(self) -> float:
        format_str = "%Y-%m-%dT%H:%M:%SZ"
        return datetime.strptime(self.updated_at, format_str).timestamp()
