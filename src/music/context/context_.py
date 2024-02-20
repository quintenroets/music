from functools import cached_property

from package_utils.context import Context as Context_

from ..clients import spotify
from ..models import Config, Options, Secrets
from ..storage.storage import Storage


class Context(Context_[Options, Config, Secrets]):
    @cached_property
    def spotify_client(self) -> spotify.Client:
        return spotify.Client(self.secrets)

    @cached_property
    def storage(self) -> Storage:
        return Storage()


context = Context(Options, Config, Secrets)
