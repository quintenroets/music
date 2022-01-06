import sys

from libs.cli import Cli

from music.path import Path

PORT = 8889
BACKEND_PORT = 9889

def main():
    debug = "debug" in sys.argv
    if debug or "restart" in sys.argv:
        clear(BACKEND_PORT, PORT)

    frontend = Path.root / "frontend" / "dist"

    commands = {
        "frontend": f"python3 -m http.server --directory {frontend} {PORT}",
        "backend": f"python3 -m uvicorn music.backend.server:app --host 0.0.0.0 --port {BACKEND_PORT}"
    }
    
    if "headless" not in sys.argv and not debug:
        Cli.start(f"http://localhost:{PORT}")

    if debug:
        commands["backend"] += f" --reload-dir {Path.root}"

    for name, command in commands.items():
        Cli.run(command, wait=debug and name=="backend")

def clear(*ports):
    for port in ports:
        command = f"lsof -t -i:{port} | xargs kill -9"
        Cli.get(command, check=False)

if __name__ == "__main__":
    main()
