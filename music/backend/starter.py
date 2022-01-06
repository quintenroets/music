import os
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
        "backend": f"python3 -m uvicorn music.backend.server:app --host 0.0.0.0 --port {BACKEND_PORT}",
        "frontend": f"python3 -m http.server --directory {frontend} {PORT}"
    }
    
    if "headless" not in sys.argv:
        commands["open"] = f"jumpapp -p -w chromium http://localhost:{PORT}"

    if debug:
        commands["backend"] += " --reload"

    for command in commands.values():
        if not debug:
            command = "nohup " + command + " &>/dev/null &"
        Cli.run(command)

def clear(*ports):
    for port in ports:
        command = f"lsof -t -i:{port} | xargs kill -9"
        Cli.get(command, check=False)

if __name__ == "__main__":
    main()
