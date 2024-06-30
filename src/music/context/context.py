from package_utils.context import Context

from music.models import Config, Options, Secrets

context = Context(Options, Config, Secrets)
