import sys
from contextlib import AbstractContextManager
from types import TracebackType

import backup.models
import cli  # pragma: nocover
from backup.main.mount import Mounter  # pragma: nocover
from backup.syncer import Syncer  # pragma: nocover
from backup.syncer.sync_configs import SyncConfigs  # pragma: nocover

from music.context import context  # pragma: nocover
from music.models import Path  # pragma: nocover


class CIContext(AbstractContextManager[None]):  # pragma: nocover
    def __init__(self) -> None:
        config = SyncConfigs.home
        config.directory = Path.assets
        self.syncer = Syncer(config)

    def __enter__(self) -> None:
        cli.console._force_terminal = True  # noqa: SLF001
        context.options.upload_to_phone = False
        remote = f"{backup.models.Path.remote}Music"
        Mounter(remote=remote, path=Path.download_assets).run()
        self.print("downloading configurations..")
        self.syncer.capture_pull()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.print("uploading results..")
        self.syncer.capture_push()

    @classmethod
    def print(cls, message: str) -> None:
        cli.console.print(message)
        sys.stdout.flush()
