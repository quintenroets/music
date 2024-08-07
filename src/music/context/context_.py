import os
from contextlib import AbstractContextManager
from functools import cached_property

from package_utils.context import Context as Context_

from music.clients import spotify
from music.models import Config, Options, Secrets
from music.storage.storage import Storage


class Context(Context_[Options, Config, Secrets]):
    @cached_property
    def spotify_client(self) -> spotify.Client:
        return spotify.Client(self.secrets)

    @cached_property
    def storage(self) -> Storage:
        return Storage()

    @cached_property
    def is_running_in_ci(self) -> bool:
        return (
            "GITHUB_ACTIONS" in os.environ and "PYTEST_CURRENT_TEST" not in os.environ
        )

    @cached_property
    def ci_context(self) -> AbstractContextManager[None] | None:
        ci_context = None
        if context.is_running_in_ci:  # pragma: nocover
            # imports optional dependencies
            try:
                from music.utils.ci_context import CIContext
            except ImportError:
                pass
            else:
                ci_context = CIContext()
        return ci_context


context = Context(Options, Config, Secrets)
