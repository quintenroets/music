from package_utils.context import Context as Context_

from ..models import Config, Options

Context = Context_[Options, Config, None]

context = Context(Options, Config)
