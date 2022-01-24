from plib import Path as BaseBasePath


class BasePath(BaseBasePath):
    @property
    def content(self):
        # cache results in json
        if not self.exists():
            self.json = self.with_suffix(".yaml").yaml
        return self.json

    @content.setter
    def content(self, value):
        self.with_suffix(".yaml").yaml = value
        self.json = value


class Path(BasePath):
    assets: BasePath = BasePath.assets / "music"
    artists = assets / "artists"
    download_ids = assets / "downloads"
    to_download = assets / "to_download"
    recommendations = assets / "recommendations"
    downloads = assets / "downloads" / "downloads"
    songs = assets / "songs" / "songs"
    env = assets / "env" / "env"
    albums = assets / "albums"

    cache = assets / ".cache"

    download_assets: BasePath = BasePath.docs / "Other" / "Music"
    downloaded_songs = download_assets / "downloads"
    processed_songs = download_assets / "processed"
    all_songs = download_assets / "all"
    deleted = download_assets / "deleted"

    root = BasePath(__file__).parent
    frontend = root / "frontend" / "dist"

    phone = "Music"
