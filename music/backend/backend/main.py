import argparse
import os
import urllib.parse
from dataclasses import dataclass

import cli
import uvicorn

from music.backend.utils import Path, config, get_backend_args


@dataclass
class Starter:
    app_name: str = "music.backend.backend:app"
    args: argparse.Namespace = None
    session_name: str = None

    def __post_init__(self):
        self.args = get_backend_args()
        self.domain_name = urllib.parse.urlparse(config.hostname).netloc
        self.session_name = self.domain_name.split(".")[0]
        self.frontend_dist = Path("/") / "var" / "www" / self.domain_name

    def start(self):
        if self.args.backend:
            self.start_backend()
        else:
            self.start_server()

    def start_backend(self):
        reload_dirs = str(Path.root / "backend") if self.args.debug else None
        log_level = "info" if self.args.debug else "warning"
        uvicorn.run(
            self.app_name,
            port=config.backend_port,
            reload_dirs=reload_dirs,
            reload=self.args.debug,
            log_level=log_level,
        )

    def start_server(self):
        if not self.args.no_frontend_check and self.is_installed():
            self.check_frontend_distribution()

        if self.args.restart:
            cli.run(f"tmux kill-session -t {self.session_name}", check=False)
        cli.run(
            f"tmux new-session -s {self.session_name} -d musicserver --backend",
            check=False,
        )
        if not self.args.headless:
            cli.urlopen(config.hostname)

    def check_frontend_distribution(self):
        if self.frontend_dist.mtime < Path.frontend.mtime:
            content_hash = Path.frontend.content_hash
            if content_hash != Path.frontend_hash.text:
                self.generate_frontend_distribution()
                Path.frontend_hash.text = content_hash
            self.frontend_dist.mtime = Path.frontend.mtime

    def generate_frontend_distribution(self):
        self.check_frontend_dist_existence()
        if cli.return_code("which npm") != 0:
            raise Exception("This project requires npm. Please install npm first")

        commands = "npm install", "npm run build"
        cli.run_commands(*commands, cwd=Path.frontend)

        # dynamically generated paths cannot be in site-packages package directory
        if self.is_installed():
            (Path.frontend / "node_modules").rmtree()

    @classmethod
    def is_installed(cls):
        return Path.root.parent.name == "site-packages"

    def check_frontend_dist_existence(self):
        if not self.frontend_dist.exists():
            username = os.getlogin()
            cli.run("mkdir", self.frontend_dist, root=True)
            cli.run(f"chown {username}:{username}", self.frontend_dist, root=True)


def main():
    Starter().start()


if __name__ == "__main__":
    main()
