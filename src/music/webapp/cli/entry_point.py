from package_utils.context.entry_point import create_entry_point

from music.webapp.context import context
from music.webapp.main.main import main

entry_point = create_entry_point(main, context)
