import os

import cli
import hostfinder
import pysftp

from ..downloads import postprocessor
from ..utils import Path


def start(fix_mtimes: bool = False, port: int = 2222) -> None:
    with cli.status("Looking for phone"):
        ip = hostfinder.find_host(port=port)
    if ip is not None:
        start_upload(ip, port=port, fix_mtimes=fix_mtimes)


def start_upload(ip: str, port: int, fix_mtimes: bool) -> None:
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    cnopts.log = True

    with cli.status("Connecting to phone"):
        sftp = pysftp.Connection(
            ip,
            port=port,
            username=os.getlogin(),
            password=cli.get("pw phone"),
            cnopts=cnopts,
        )
    with sftp:
        process_remote_deletes(sftp, fix_mtimes)
        upload(sftp)


def upload(sftp: pysftp.Connection) -> None:
    sftp.makedirs(Path.phone)

    downloads = list(Path.processed_songs.glob("*.opus"))  # make list to know length
    downloads = cli.progress(
        downloads, description="Copying to phone", unit="songs", cleanup=True
    )
    for song in downloads:
        sftp.put(
            localpath=song, remotepath=f"{Path.phone}/{song.name}", preserve_mtime=True
        )
        song.rename(Path.all_songs / song.name)


def process_remote_deletes(sftp: pysftp.Connection, fix_mtimes: bool) -> None:
    with cli.console.status("Checking remote deletes"):
        phone_songs = sftp.listdir(Path.phone)

    if fix_mtimes and False:
        for path in Path.all_songs.iterdir():
            postprocessor.process_download(path, set_title=False)

    songs = Path.all_songs.iterdir()
    if fix_mtimes:
        songs = cli.progress(list(songs), description="fixing mtime", unit="songs")

    for song in songs:
        if song.name not in phone_songs:
            print(f"Removing {song.stem}")
            song.rename(Path.deleted / song.name)

        elif fix_mtimes:
            remote_path = f"{Path.phone}/{song.name}"
            mtime = sftp.stat(remote_path).st_mtime
            if int(mtime) != int(song.mtime):
                print(song.name)
                mtime = max(song.mtime, 0)
                times = (mtime, mtime)
                sftp._sftp.utime(remote_path, times)


if __name__ == "__main__":
    start()
