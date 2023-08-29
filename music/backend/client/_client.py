import logging
import time

import requests
import spotipy
from retry import retry
from spotipy.cache_handler import CacheFileHandler
from spotipy.oauth2 import SpotifyClientCredentials

from music.backend.utils import Path, tokens


class Spotify(spotipy.Spotify):
    def __init__(self, market="BE"):
        self.market = market
        ccm = SpotifyClientCredentials(
            client_id=tokens.spotify.client_id,
            client_secret=tokens.spotify.client_secret,
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
    def _internal_call(self, method, url, payload, params):
        try:
            for market_param in ("country", "market"):
                if market_param in params:
                    params[market_param] = self.market
            response = super()._internal_call(method, url, payload, params)
            return response
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status in (404, 429):
                # include 404 status because spotify api sometimes returns 404 error
                # when it should be 429
                # https://community.spotify.com/t5/Spotify-for-Developers/
                # Intermittent-404s-Getting-Playlist-Tracks-via-API/m-p/5356770
                time.sleep(2)
                raise requests.exceptions.ReadTimeout
            else:
                raise
