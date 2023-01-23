import sys

import cli

import music
from music.artist import ArtistManager, Artists
from music.client import spotapi


def main():
    if "add" in sys.argv:
        add_new_songs(sys.argv[2:])
    elif music.Path.processed_songs.is_empty() and not music.Path.to_download.yaml:
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


def add_new_songs(names):
    new_songs = []
    for name in names:
        song_results = spotapi.search_song(name)
        see_next = True

        for song in song_results:
            if see_next:
                see_next = False
                full_name = music.downloads.jobs.full_name(song)
                if cli.confirm(f"{full_name}\nDownload?"):
                    new_songs.append(song)
                elif cli.confirm("See next result"):
                    see_next = True

    music.downloads.jobs.add(new_songs)


if __name__ == "__main__":
    main()
