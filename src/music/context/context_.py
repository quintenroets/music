from package_utils.context import Context as Context_

from .config import Config
from .options import Options
from .secrets_ import Secrets

Context = Context_[Options, Config, Secrets]

context = Context(Options, Config, Secrets)
