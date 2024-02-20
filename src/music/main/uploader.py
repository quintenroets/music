import os
from collections.abc import Iterator
from dataclasses import dataclass
from functools import cached_property

import cli
import hostfinder
import pysftp

from ..context import context
from ..download.downloaded_songs_processor import DownloadedTrackProcessor
from ..models import Path


def start() -> None:  # pragma: nocover
    with cli.status("Looking for phone"):  # type: ignore
        ip = hostfinder.find_host(port=context.config.phone_upload_port)
    if ip is not None:
        Uploader(ip).run()


@dataclass
class Uploader:  # pragma: nocover
    ip: str

    def __post_init__(self) -> None:
        with cli.status("Connecting to phone"):  # type: ignore
            self.phone_connection = self.create_phone_connection()

    @property
    def phone_connection_options(self) -> pysftp.CnOpts:
        connection_options = pysftp.CnOpts()
        connection_options.hostkeys = None
        connection_options.log = True
        return connection_options

    def create_phone_connection(self) -> pysftp.Connection:
        username = None if "GITHUB_ACTIONS" in os.environ else os.getlogin()
        return pysftp.Connection(
            self.ip,
            port=context.config.phone_upload_port,
            username=username,
            password=context.secrets.phone_connection,
            cnopts=self.phone_connection_options,
        )

    def run(self) -> None:
        with self.phone_connection:
            self._run()

    def _run(self) -> None:
        self.phone_connection.makedirs(Path.phone)
        if context.options.fix_mtimes_on_phone:
            self.fix_mtimes_on_phone()
        self.process_remote_deletes()
        self.upload_new_songs()

    def fix_mtimes_on_phone(self) -> None:
        for path in Path.all_songs.iterdir():
            DownloadedTrackProcessor(path, set_title=False).run()

        description = "Fixing mtime of all songs on phone"
        song_paths = Path.all_songs.iterdir()
        song_paths = self.iterate_over_song_paths(song_paths, description=description)

        for path in song_paths:
            self.fix_mtime_on_phone(path)

    def fix_mtime_on_phone(self, path: Path) -> None:
        remote_path = f"{Path.phone}/{path.name}"
        mtime = self.phone_connection.stat(remote_path).st_mtime
        if mtime is None or int(mtime) != int(path.mtime):
            fixed_mtime = max(path.mtime, 0)
            fixed_mtimes = (fixed_mtime, fixed_mtime)
            self.phone_connection._sftp.utime(remote_path, fixed_mtimes)  # type: ignore

    @classmethod
    def iterate_over_all_songs(cls, description: str) -> Iterator[Path]:
        paths = Path.all_songs.iterdir()
        paths_with_length = list(paths)
        yield from cli.progress(  # type: ignore
            paths_with_length, description=description, unit="songs", cleanup=True
        )

    def process_remote_deletes(self) -> None:
        songs = Path.all_songs.iterdir()
        for song in songs:
            if song.name not in self.uploaded_song_names:
                print(f"Removing {song.stem}")
                song.rename(Path.deleted / song.name)

    @cached_property
    def uploaded_song_names(self) -> set[str]:
        with cli.console.status("Reading songs on phone"):
            uploaded_names = self.phone_connection.listdir(Path.phone)
        return set(uploaded_names)

    def upload_new_songs(self) -> None:
        description = "Copying new songs to phone"
        new_song_paths = Path.processed_songs.glob("*.opus")
        new_song_paths = self.iterate_over_song_paths(
            new_song_paths, description=description
        )
        for path in new_song_paths:
            self.upload_song(path)

    @classmethod
    def iterate_over_song_paths(
        cls, paths: Iterator[Path], description: str
    ) -> Iterator[Path]:
        paths_with_length = list(paths)
        yield from cli.progress(  # type: ignore
            paths_with_length, description=description, unit="songs", cleanup=True
        )

    def upload_song(self, path: Path) -> None:
        self.phone_connection.put(
            localpath=str(path),
            remotepath=f"{Path.phone}/{path.name}",
            preserve_mtime=True,
        )
        path.rename(Path.all_songs / path.name)
