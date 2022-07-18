from plib import Path as BaseBasePath


class BasePath(BaseBasePath):
    @property
    def content(self) -> dict:
        # cache results in json
        if self.mtime < self.with_suffix(".yaml").mtime:
            self.json = self.with_suffix(".yaml").yaml
        return self.json

    @content.setter
    def content(self, value):
        self.with_suffix(".yaml").yaml = value
        self.json = value


class Path(BasePath):
    assets: BasePath = BasePath.assets / "music"

    download_info = assets / "downloads"
    download_ids = download_info / "ids"
    fails = download_info / "fails"
    to_download = assets / "cache" / "to_download"

    artist_assets = assets / "artists"
    artists = artist_assets / "artists"
    recommendations = artist_assets / "recommendations"

    env = assets / "env" / "env"
    cache_assets = assets / "cache"
    cache = cache_assets / ".cache"

    download_assets: BasePath = BasePath.docs / "Backup" / "Music"
    downloaded_songs = download_assets / "downloads"
    processed_songs = download_assets / "processed"
    all_songs = download_assets / "all"
    deleted = download_assets / "deleted"

    root = BasePath(__file__).parent
    frontend = root / "frontend" / "dist"

    phone = "Music"
