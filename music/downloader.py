import sys
import requests

from libs.cli import Cli

from .datamanager import DataManager
from .path import Path

class Downloader:
    @staticmethod
    def download(new_songs):
        output_path = Path.downloaded_songs
        output_path.mkdir(parents=True, exist_ok=True)
        options = {
            "output-format": "opus",
            "output": output_path,
            "download-threads": "10",
            "search-threads": "10"
        }
        options = [f"--{k} {v}" for k, v in options.items()]
        songs_commands = [
            f'"{id_}"' if "http" in id_ else "https://open.spotify.com/track/" + id_  for id_ in new_songs
        ]

        old_length, new_length = 0, len(songs_commands)
        while songs_commands and old_length != new_length:
            Downloader.run_with_retry(
                "spotdl " + " ".join(options + songs_commands)
            )
            songs_commands = [f'"{incomplete}"' for incomplete in output_path.glob("*.spotdlTrackingFile")]
            old_length, new_length = new_length, len(songs_commands)

    @staticmethod
    def run_with_retry(command):
        while True:
            try:
                return Cli.run(command)
            except KeyError: # make interuptable
                raise KeyError
            except:# requests.exceptions.ReadTimeout:
                Cli.run("clear")
