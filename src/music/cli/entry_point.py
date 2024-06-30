from package_utils.context.entry_point import create_entry_point

from music import main
from music.context import context

entry_point = create_entry_point(main, context)
