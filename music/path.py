from plib import Path as BaseBasePath


class BasePath(BaseBasePath):
    @property
    def yaml(self) -> dict:
        # cache results in json
        json_path = self.with_suffix(".json")
        if json_path.mtime < self.mtime:
            content = self.yaml
            json_path.json = content
        else:
            content = self.json_path
        return content

    @yaml.setter
    def yaml(self, value):
        self.yaml = value
        self.with_suffix(".json").json = value


class Path(BasePath):
    assets: BasePath = BasePath.assets / "music"

    download_info = assets / "downloads"
    download_ids = download_info / "ids.yaml"
    fails = download_info / "fails.yaml"
    to_download = assets / "cache" / "to_download.yaml"

    artist_assets = assets / "artists"
    artists = artist_assets / "artists.yaml"
    recommendations = artist_assets / "recommendations.yaml"

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
