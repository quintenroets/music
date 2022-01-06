import lyricsgenius
import os


class LyricsManager:
    genius = lyricsgenius.Genius(os.environ["GENIUS_TOKEN"])
    genius.skip_non_songs = True
    genius.verbose = False  # to print search statement

    @staticmethod
    def get_lyrics(artist, title, tries=10):
        for _ in range(tries):
            try:
                song = LyricsManager.genius.search_song(title, artist, get_full_info=False)
            except requests.exceptions.Timeout:
                pass
            else:
                lyrics = song.lyrics
                if lyrics and len(lyrics) > 200:
                    return lyrics
