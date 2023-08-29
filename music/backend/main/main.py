import sys

import cli

from ..artist import ArtistManager, Artists
from ..client import spotapi
from ..downloads import download as start_downloads
from ..downloads import jobs
from ..utils import Path, get_args


def main():
    args = get_args()
    if args.add is not None:
        add_new_songs([args.add])

    no_phone_needed = Path.processed_songs.is_empty() or args.no_phone
    new_songs_needed = no_phone_needed and not Path.to_download.yaml
    if new_songs_needed:
        collect_new_songs()

    start_downloads()

    if "hang" in sys.argv:
        print("Press key to exit")
        input("$ ")


def collect_new_songs():
    artists = Artists()
    artists = cli.progress(
        artists, description="Checking new songs", unit="artists", cleanup=True
    )
    for artist in artists:
        ArtistManager(artist).collect_new_songs()


def add_new_songs(names):
    new_songs = []
    for name in names:
        song_results = spotapi.search_song(name)
        see_next = True

        for song in song_results:
            if see_next:
                see_next = False
                full_name = jobs.full_name(song)
                if cli.confirm(f"{full_name}\nDownload?"):
                    new_songs.append(song)
                elif cli.confirm("See next result"):
                    see_next = True

    jobs.add(new_songs)


if __name__ == "__main__":
    main()
