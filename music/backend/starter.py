import sys

from libs.cli import Cli

from music.path import Path

PORT = 8889
BACKEND_PORT = 9889

def main():
    debug = "debug" in sys.argv
    if debug or "restart" in sys.argv:
        clear(BACKEND_PORT, PORT)

    Cli.run(f"python3 -m http.server --directory {Path.frontend} {PORT}", wait=False)

    command = f"python3 -m uvicorn music.backend.server:app --host 0.0.0.0 --port {BACKEND_PORT}"
    if debug:
        command += f" --reload-dir {Path.root}"
    Cli.run(command, wait=debug)
    
    if "headless" not in sys.argv and not debug:
        Cli.start(f"http://localhost:{PORT}")

def clear(*ports):
    for port in ports:
        command = f"lsof -t -i:{port} | xargs kill -9"
        Cli.get(command, check=False)

if __name__ == "__main__":
    main()
