from .artist import Artist, FAVORITE
from music.path import Path
from music.client import spotapi
from music.downloads import jobs


class ArtistPaths:
    def __init__(self, name):
        self.name = name.replace("/", "")

    @property
    def albums(self):
        return Path.assets / "albums" / self.name

    @property
    def album_count(self):
        return Path.assets / "album_counts" / self.name

    @property
    def top_songs(self):
        return Path.assets / "top_songs" / self.name


def unique(items):
    sorted_items = sorted(
        items, key=lambda item: item.release_date, reverse=True
    )  # first sort from new to old
    unique_items = {
        item.name: item for item in sorted_items
    }  # Unique by name and choose oldest if duplicates
    unique_items = list(unique_items.values())  # convert to list
    return unique_items


class ArtistManager(Artist):
    def __init__(self, artist):
        super().__init__(**artist.__dict__)
        self.path = ArtistPaths(self.name)

    def collect_new_songs(self):
        if self.type == FAVORITE:
            self.check_all_songs()
        else:
            self.check_top_songs()

    def check_top_songs(self):
        cached_songs = self.path.top_songs.content
        songs = spotapi.top_songs(self.id)
        new_songs = [s for s in songs if s.id not in cached_songs]
        jobs.add(new_songs)
        self.path.top_songs.content |= {s.id: s.name for s in new_songs}

    def check_all_songs(self):
        album_count = self.path.album_count.content or 0
        if spotapi.album_count(self.id) > album_count:
            albums = self.path.albums.content
            for album_type in ["album", "single"]:
                new_amount = spotapi.album_count(
                    self.id, album_type=album_type
                ) - albums.get(album_type, 0)
                if new_amount > 0:
                    new_albums = spotapi.albums(
                        self.id, album_type=album_type, amount=new_amount
                    )
                    for album in unique(new_albums):
                        songs = spotapi.album_songs(album)
                        songs = spotapi.songs(
                            [song.id for song in songs]
                        )  # popularity and release_date needed

                        jobs.add(songs)
                        album_songs = {s.id: s.name for s in songs}
                        self.path.albums.content |= {album.id: album_songs}

                    self.path.album_count.content = self.path.album_count.content + len(
                        new_albums
                    )


"""

        from rich.pretty import pprint
        for s in songs:
            found = False
            for artists in [s.artists, s.artists[:1]]:
                name = ', '.join([a.name for a in artists]) + ' - ' + s.name + '.opus'
                path = (Path.all_songs / name)
                if path.exists():
                    found = True

            if not found:
                s = spotapi.songs([s.id])[0]
                if not download_wanted(s):
                    found = True
            found = True
            if not found:
                import cli
                cli.console.clear()
                pprint(path.name)
                pprint(s)
                cli.run('chromium', s.external_urls.spotify)
                found = input('skip? [Y]') == ''
                print(found)

            if found:
                cached_songs[s.id] = s.name
"""
