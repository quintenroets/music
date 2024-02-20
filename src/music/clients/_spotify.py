import logging
import os
import random
import time
from dataclasses import dataclass

import requests
import spotipy
from retry import retry
from spotipy.cache_handler import CacheFileHandler
from spotipy.oauth2 import SpotifyClientCredentials

from ..models import Path, Secrets


@dataclass
class Spotify(spotipy.Spotify):  # type: ignore
    secrets: Secrets
    market: str = "BE"

    def __post_init__(self) -> None:
        ccm = SpotifyClientCredentials(
            client_id=self.secrets.spotify.client_id,
            client_secret=self.secrets.spotify.client_secret,
            cache_handler=CacheFileHandler(Path.cache),
        )
        super().__init__(
            client_credentials_manager=ccm,
            requests_timeout=1,
            status_retries=0,
            retries=3,
            backoff_factor=1,
        )
        logging.disable()  # ignore retry error log messages from spotify library

    @retry(requests.exceptions.ReadTimeout, tries=10)
    def _internal_call(
        self, method: str, url: str, payload: dict[str, str], params: dict[str, str]
    ) -> dict[str, str] | None:
        try:
            for market_param in ("country", "market"):
                if market_param in params:
                    params[market_param] = self.market
            response = super()._internal_call(method, url, payload, params)
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status in (404, 429):
                # include 404 status because spotify api sometimes returns 404 error
                # when it should be 429
                # https://community.spotify.com/t5/Spotify-for-Developers/
                # Intermittent-404s-Getting-Playlist-Tracks-via-API/m-p/5356770
                self.sleep()  # pragma: nocover
                raise requests.exceptions.ReadTimeout  # pragma: nocover
            else:
                raise
        return response  # type: ignore

    @classmethod
    def sleep(cls) -> None:  # pragma: nocover
        time.sleep(2)
        if "GITHUB_ACTION" in os.environ:
            # Unit tests lead to rate limits because all requests start at the same time
            extra_time = 5 + random.Random().random() * 10
            time.sleep(extra_time)
