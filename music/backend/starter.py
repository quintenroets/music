import cli
import sys

from music.path import Path

PORT = 8889
BACKEND_PORT = 9889

def main():
    debug = 'debug' in sys.argv
    if debug or 'restart' in sys.argv:
        for port in PORT, BACKEND_PORT:
            clear(port)

    cli.start('python3 -m http.server --directory', Path.frontend, PORT)

    command = f'python3 -m uvicorn music.backend.server:app --host 0.0.0.0 --port {BACKEND_PORT}'
    if debug:
        command += f' --reload-dir {Path.root}'
    cli.run(command, wait=debug)
    
    if 'headless' not in sys.argv and not debug:
        cli.urlopen(f'http://localhost:{PORT}')


def clear(port):
    cli.get(f'lsof -t -i:{port} | xargs kill -9', check=False, shell=True)


if __name__ == '__main__':
    main()
