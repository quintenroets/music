from setuptools import setup, find_packages

NAME = "music"


def read(filename):
    try:
        with open(filename) as fp:
            content = fp.read().split("\n")
    except FileNotFoundError:
        content = []
    return content


setup(
    author="Quinten Roets",
    author_email="quinten.roets@gmail.com",
    description="",
    name=NAME,
    version="1.0",
    packages=find_packages(),
    package_data={
        "music": [
            "frontend/dist/*",
            "frontend/dist/css/*",
            "frontend/dist/img/*",
            "frontend/dist/js/*",
        ]
    },
    install_requires=read("requirements.txt"),
    setup_requires=read("setup_requirements.txt"),
    entry_points={
        "console_scripts": [
            "music = music.main:main",
            "musicserver = music.backend.starter:main",
        ]
    },
)

import cli

cli.install(*read("packages.txt"))
cli.run_commands("npm install", "npm run build", cwd="music/frontend")
