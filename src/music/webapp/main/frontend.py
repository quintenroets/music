import io
import os
import urllib.parse
import zipfile
from dataclasses import dataclass, field

import cli
import requests
from plib import Path

from music.webapp.context import context

from .frontend_release import FrontendRelease


def load_dist_path() -> Path:
    domain_name = urllib.parse.urlparse(context.config.hostname).netloc
    return Path("/") / "var" / "www" / domain_name


@dataclass
class Frontend:
    content_path: Path = field(default_factory=load_dist_path)

    @classmethod
    def check_content(cls) -> None:
        frontend = Frontend()
        if context.options.update_frontend or not frontend.content_path.exists():
            frontend.update_content()

    def update_content(self) -> None:
        frontend_release = FrontendRelease.load()
        if self.content_path.mtime < frontend_release.mtime:
            self.download_content(frontend_release)

    def download_content(self, frontend_release: FrontendRelease) -> None:
        if not self.content_path.exists():
            self.create_content_path()
        content = requests.get(frontend_release.browser_download_url).content
        content_io = io.BytesIO(content)
        zip_file = zipfile.ZipFile(content_io)
        with zip_file:
            zip_file.extractall(self.content_path)
        self.content_path.mtime = frontend_release.mtime

    def create_content_path(self) -> None:
        try:
            username = os.getlogin()
        except OSError:  # pragma: nocover (on GitHub action)
            username = "runner"  # pragma: nocover
        cli.run("mkdir", self.content_path, root=True)
        cli.run(f"chown -R {username}:{username}", self.content_path, root=True)
