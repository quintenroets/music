import logging
import os
import requests
import spotipy

from dotenv import load_dotenv
from retry import retry
from spotipy.cache_handler import CacheFileHandler
from spotipy.oauth2 import SpotifyClientCredentials
from music.path import Path


class Spotify(spotipy.Spotify):
    def __init__(self, market="BE"):
        self.market = market
        load_dotenv(dotenv_path=Path.env)

        ccm = SpotifyClientCredentials(
            client_id=os.environ["SPOTAPI_ID"],
            client_secret=os.environ["SPOTAPI_SECRET"],
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

    @retry(spotipy.exceptions.SpotifyException, delay=2)
    @retry(requests.exceptions.ReadTimeout)
    def _internal_call(self, method, url, payload, params):
        for market_param in ("country", "market"):
            if market_param in params:
                params[market_param] = self.market
        response = super()._internal_call(method, url, payload, params)
        return response
