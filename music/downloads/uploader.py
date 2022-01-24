import cli
import os
import pysftp

from libs.portscanner import Scanner
from music.path import Path


def start():
    with cli.console.status("Looking for phone"):
        ip = Scanner.get_ip(port=2222)
    if ip is not None:
        start_upload(ip)


def start_upload(ip):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    cnopts.log = True

    sftp = pysftp.Connection(
        ip, port=2222, username=os.getlogin(), password=os.environ["pw"], cnopts=cnopts
    )
    with sftp:
        process_remote_deletes(sftp)
        upload(sftp)


def upload(sftp):
    sftp.makedirs(Path.phone)

    downloads = list(Path.processed_songs.glob("*.opus"))  # make list to know length
    downloads = cli.progress(downloads, description="Copying to phone", unit="songs")
    for song in downloads:
        sftp.put(
            localpath=song, remotepath=f"{Path.phone}/{song.name}", preserve_mtime=True
        )
        song.rename(Path.all_songs / song.name)


def process_remote_deletes(sftp):
    with cli.console.status("Checking remote deletes"):
        phone_songs = sftp.listdir(Path.phone)

    for song in Path.all_songs.iterdir():
        if song.name not in phone_songs:
            print(f"Removing {song.stem}")
            song.rename(Path.deleted / song.name)
