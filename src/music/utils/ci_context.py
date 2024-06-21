from types import TracebackType

import backup.models
import cli
from backup.backup import Backup
from backup.main.mount import Mounter

from music.models import Path

from ..context import context


class CIContext:  # pragma: nocover
    def __init__(self) -> None:
        remote_home = backup.models.Path.remote / "home" / "quinten"
        dest = remote_home / Path.assets.relative_to(Path.HOME)
        self.backup = Backup(source=Path.assets, dest=dest)

    def __enter__(self) -> None:
        cli.console._force_terminal = True
        context.options.upload_to_phone = False
        Mounter(remote="ColumbiaBackup:Music", path=Path.download_assets).run()
        self.backup.pull()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.backup.push()
