import sys

import cli

from music.path import Path

PORT = 8889
BACKEND_PORT = 9889


def main():
    debug = "debug" in sys.argv
    if debug or "restart" in sys.argv:
        for port in PORT, BACKEND_PORT:
            clear(port)

    check_frontend_compilation()

    if not cli.get(f"lsof -t -i:{PORT}", check=False):
        cli.start("python3 -m http.server --directory", Path.frontend, PORT)

    command = (
        "python3 -m uvicorn music.backend.server:app --host 0.0.0.0 --port"
        f" {BACKEND_PORT}"
    )
    if debug:
        command += f" --reload-dir {Path.root}"
    cli.run(command, wait=debug)

    if "headless" not in sys.argv and not debug:
        cli.urlopen(f"http://localhost:{PORT}")


def clear(port):
    cli.get(f"lsof -t -i:{port} | xargs kill -2", check=False, shell=True)


def check_frontend_compilation():
    if not Path.frontend.exists():
        if cli.return_code("which npm") != 0:
            raise Exception("This project requires npm. Please install npm first")

        cli.run("npm install; npm run build", cwd=Path.frontend.parent, shell=True)


if __name__ == "__main__":
    main()
