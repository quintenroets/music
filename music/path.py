from plib import Path as BasePath


class Path(BasePath):
    assets = BasePath.assets / "music"
    artists = assets / "artists" / "artists"
    recommendations = assets / "artists" / "recommendations"
    downloads = assets / "downloads" / "downloads"
    album_counts = assets / "albums"
    songs = assets / "songs" / "songs"
    env = assets / "env" / "env"

    download_assets = BasePath.docs / "Other" / "Music"
    downloaded_songs = download_assets / "downloads"
    all_songs = download_assets / "all"

    root = BasePath(__file__).parent
