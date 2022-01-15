import cli
import requests
import sys

from .datamanager import DataManager
from .path import Path


class Downloader:
    @staticmethod
    def download(new_songs):
        output_path = Path.downloaded_songs
        output_path.mkdir(parents=True, exist_ok=True)
        for p in output_path.glob("*"):
            p.unlink() # existing downloads raise errors
        
        options = {
            "output-format": "opus",
            "output": output_path,
            "download-threads": "10",
            "search-threads": "10"
        }
        songs_commands = [
            id_ if "http" in id_ else "https://open.spotify.com/track/" + id_  for id_ in new_songs
        ]

        old_length, new_length = 0, len(songs_commands)
        while songs_commands and old_length != new_length:
            Downloader.run_with_retry('spotdl', options, songs_commands)
            songs_commands = list(output_path.glob("*.spotdlTrackingFile"))
            old_length, new_length = new_length, len(songs_commands)

    @staticmethod
    def run_with_retry(command):
        while True:
            try:
                return cli.run(command)
            except KeyboardInterrupt: # make interuptable
                raise KeyboardInterrupt
            except requests.exceptions.ReadTimeout:
                cli.run("clear")
