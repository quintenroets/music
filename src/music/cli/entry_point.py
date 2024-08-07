import os

from package_utils.context.entry_point import Context, create_entry_point

from music.context import context
from music.main import main
from music.models import Config, Options, Secrets


def configure_no_secret_file(context: Context[Options, Config, Secrets]) -> None:
    if "GITHUB_ACTIONS" in os.environ:
        context.config.secrets_path = None  # pragma: nocover


entry_point = create_entry_point(
    main,
    context,
    context_creation_callback=configure_no_secret_file,
)
