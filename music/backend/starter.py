import argparse

import cli
import uvicorn

from music.path import Path

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
    host = "0.0.0.0"
    uvicorn.run(
        module, host=host, port=BACKEND_PORT, reload_dirs=reload_dirs, reload=args.debug
    )


def start_server(args):
    check_frontend_compilation()
    if args.restart:
        for port in (BACKEND_PORT, PORT):
            clear(port)

    if not port_occupied(PORT):
        cli.start("python3 -m http.server", PORT, {"directory": Path.frontend})

    if not port_occupied(BACKEND_PORT):
        start = cli.run if args.debug else cli.start
        start("musicserver backend")

    if not args.headless:
        cli.urlopen(f"http://localhost:{PORT}")


def port_occupied(port):
    return cli.get(f"lsof -t -i:{port}", check=False)


def clear(port):
    cli.get(f"lsof -t -i:{port} | xargs kill -2", check=False, shell=True)


def check_frontend_compilation():
    if not Path.frontend.exists():
        if cli.return_code("which npm") != 0:
            raise Exception("This project requires npm. Please install npm first")

        cli.run("npm install; npm run build", cwd=Path.frontend.parent, shell=True)


if __name__ == "__main__":
    main()
