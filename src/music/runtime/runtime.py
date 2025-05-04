import os
from contextlib import AbstractContextManager
from functools import cached_property
from typing import TYPE_CHECKING

from music.clients import spotify
from music.context import Context, context
from music.storage.storage import Storage

if TYPE_CHECKING:
    from spotdl.providers.audio import YouTubeMusic  # pragma: nocover


class Runtime:
    def __init__(self) -> None:
        self.context: Context = context

    @cached_property
    def spotify_client(self) -> spotify.Client:
        return spotify.Client(self.context.secrets)

    @cached_property
    def youtube_music_client(self) -> "YouTubeMusic":
        # slow import
        from spotdl.providers.audio.ytmusic import YouTubeMusic

        return YouTubeMusic()

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


runtime = Runtime()
