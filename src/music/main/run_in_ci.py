from collections.abc import Iterable
from ..context import context
from typing import TypeVar

import cli


from backup.main.mount import Mounter

from backup.backup import Backup
from music.models import Path


from . import _main


def main() -> None:
    Mounter(remote_name="ColumbiaBackup:Music", path=Path.download_assets).run()
    dest = f"backup:home/quinten/{Path.assets.relative_to(Path.HOME)}"
    backup = Backup(source=Path.assets, dest=dest)
    backup.pull()
    context.options.upload_to_phone = False
    _main.main()
    backup.push()
