import uvicorn

from music.webapp.context import context

from ..models import Path


def main() -> None:
    reload_dirs = str(Path.source_root) if context.options.debug else None
    log_level = "info" if context.options.debug else "warning"
    uvicorn.run(
        context.config.app_name,
        port=context.config.backend_port,
        reload_dirs=reload_dirs,
        reload=context.options.debug,
        log_level=log_level,
    )
