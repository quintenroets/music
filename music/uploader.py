import os
import pysftp

from libs.progressbar import ProgressBar
from libs.portscanner import Scanner

from .datamanager import DataManager
from .path import Path

class Uploader:
    @staticmethod
    def start():
        with ProgressBar("Music", message="Finding phone"):
            ip = Scanner.get_ip(port=2222)
        if ip is not None:
            Uploader.start_upload(ip)

    @staticmethod
    def start_upload(ip):
        print("Phone found")

        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        cnopts.log = True

        with pysftp.Connection(
            ip,
            port=2222,
            username=os.getlogin(),
            password=os.environ["pw"],
            cnopts=cnopts
        ) as sftp:
            if sftp:
                Uploader.process_remote_deletes(sftp)
                Uploader.upload(sftp)

    @staticmethod
    def upload(sftp):
        downloads = list(DataManager.get_downloaded_songs()) # make list to know length
        iterator = ProgressBar(downloads, title="Music", message="copying to phone", progress_name="songs")
        phone_folder = "Music"

        sftp.makedirs(phone_folder)
        Path.all_songs.mkdir(parents=True, exist_ok=True)

        for song in iterator:
            if song.stat().st_size:
                sftp.put(localpath=song, remotepath=f"{phone_folder}/{song.name}", preserve_mtime=True)
                song.rename(Path.all_songs / song.name)
            else:
                song.unlink()

    @staticmethod
    def process_remote_deletes(sftp):
        phone_folder = "Music"
        phone_songs = sftp.listdir(phone_folder)
        Path.all_songs.mkdir(parents=True, exist_ok=True)

        for song in Path.all_songs.iterdir():
            if song.name not in phone_songs:
                print(f"Removing {song.stem}")
                song.unlink()
