from collections.abc import Iterator

import cli

from music.webapp.context import context

from .frontend import Frontend


def main() -> None:
    start_backend()
    open_frontend()


def open_frontend() -> None:
    Frontend.check_content()
    if not context.options.headless:
        cli.urlopen(context.config.hostname)


def start_backend() -> None:
    commands = generate_commands()
    cli.run_commands(*commands)


def generate_commands() -> Iterator[str]:
    backend_command = "music-backend"
    session_name = context.config.session_name or backend_command
    if context.options.restart:
        yield f"tmux kill-session -t {session_name}"

    yield f"tmux new-session -s {session_name} -d {backend_command}"
