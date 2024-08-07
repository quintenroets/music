import sys
from contextlib import AbstractContextManager
from types import TracebackType

import backup.models
import cli  # pragma: nocover
from backup.backup import Backup  # pragma: nocover
from backup.main.mount import Mounter  # pragma: nocover

from music.context import context  # pragma: nocover
from music.models import Path  # pragma: nocover


class CIContext(AbstractContextManager[None]):  # pragma: nocover
    def __init__(self) -> None:
        remote_home = backup.models.Path.remote / "home" / "quinten"
        dest = remote_home / Path.assets.relative_to(Path.HOME)
        self.backup = Backup(source=Path.assets, dest=dest)

    def __enter__(self) -> None:
        cli.console._force_terminal = True  # noqa: SLF001
        context.options.upload_to_phone = False
        Mounter(remote="ColumbiaBackup:Music", path=Path.download_assets).run()
        self.print("downloading configurations..")
        self.backup.capture_pull()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.print("uploading results..")
        self.backup.capture_push()

    @classmethod
    def print(cls, message: str) -> None:
        cli.console.print(message)
        sys.stdout.flush()
