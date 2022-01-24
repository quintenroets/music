import cli

from music.path import Path


def download_wanted(song):
    skip_names = ("Interlude", "Intro", "Outro", "Live", "Instrumental")
    return (
        2 * 60 * 1000 < song.duration_ms < 10 * 60 * 1000
        and song.popularity > 15
        and not any([f" - {skip_name}" in song.name for skip_name in skip_names])
    )


def add(songs, urls=False):
    if songs:
        if urls:
            songs = {song: "" for song in songs}
        else:
            songs = sorted(songs, key=lambda song: song.popularity, reverse=True)
            songs = {
                song.id: f"{song.name} - {song.artists[0].name}"
                for song in songs
                if download_wanted(song)
            }
            for name in songs.values():
                cli.console.print(name)

        downloads = Path.download_ids.content
        new_songs = {k: v for k, v in songs.items() if k not in downloads}

        Path.download_ids.content |= new_songs
        Path.to_download.content |= new_songs


def get():
    return list(Path.to_download.content.keys())


def remove(songs):
    Path.to_download.content = {
        k: v for k, v in Path.to_download.content.items() if k not in songs
    }
