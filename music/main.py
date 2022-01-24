import sys

import cli
import music
from music.artist import ArtistManager, Artists


def main():
    if "add" in sys.argv[2:]:
        music.downloads.jobs.add(sys.argv[2:], urls=True)
    elif music.Path.processed_songs.is_empty() and not music.Path.to_download.content:
        collect_new_songs()

    music.start_downloads()

    if "hang" in sys.argv:
        print("Press key to exit")
        input("$ ")


def collect_new_songs():
    artists = Artists()
    artists = cli.progress(artists, description="Checking new songs", unit="artists")
    for artist in artists:
        ArtistManager(artist).collect_new_songs()


if __name__ == "__main__":
    main()
