import argparse

import cli
import dirhash
import uvicorn

from music.utils import Path

PORT = 8889
BACKEND_PORT = 9889


def get_args():
    parser = argparse.ArgumentParser(description="Music")
    parser.add_argument("options", nargs="*", default=[])
    args = parser.parse_args()
    args.backend = "backend" in args.options
    args.debug = "debug" in args.options
    args.restart = "restart" in args.options or args.debug
    args.backend = "backend" in args.options
    args.headless = "headless" in args.options or args.debug
    return args


def main():
    args = get_args()
    if args.backend:
        start_backend(args)
    else:
        start_server(args)


def start_backend(args):
    reload_dirs = (Path.root / "backend",) if args.debug else None
    module = "music.backend.server:app"
    uvicorn.run(module, port=BACKEND_PORT, reload_dirs=reload_dirs, reload=args.debug)


def start_server(args):
    check_frontend_distribution()
    if args.restart:
        for port in (BACKEND_PORT, PORT):
            clear(port)

    if not port_occupied(PORT):
        cli.start("python3 -m http.server", PORT, {"directory": Path.frontend_dist})

    if not port_occupied(BACKEND_PORT):
        start = cli.run if args.debug else cli.start
        start("musicserver backend")

    if not args.headless:
        cli.urlopen(f"http://localhost:{PORT}")


def port_occupied(port):
    return cli.get(f"lsof -t -i:{port}", check=False)


def clear(port):
    cli.get(f"lsof -t -i:{port} | xargs kill -2", check=False, shell=True)


def check_frontend_distribution():
    if Path.frontend_dist.mtime < Path.frontend.mtime:
        frontend_hash = dirhash.dirhash(Path.frontend, "sha1")
        if frontend_hash != Path.frontend_hash.text:
            generate_frontend_distribution()
            Path.frontend_hash.text = frontend_hash


def generate_frontend_distribution():
    if cli.return_code("which npm") != 0:
        raise Exception("This project requires npm. Please install npm first")

    commands = "npm install", "npm run build"
    cli.run_commands(*commands, cwd=Path.frontend)
    # dynamically generated paths cannot be in package directory
    (Path.frontend / "node_modules").rmtree()
    (Path.frontend / "dist").rename(Path.frontend_dist)


if __name__ == "__main__":
    main()
