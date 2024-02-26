from package_utils.context.entry_point import create_entry_point
from webapp_starter.context.context import Context_, context
from webapp_starter.main.main import main
from webapp_starter.models import Config, Options


def add_name(created_context: Context_[Options, Config, None]) -> None:
    created_context.options.name = "music"


entry_point = create_entry_point(main, context, context_creation_callback=add_name)
