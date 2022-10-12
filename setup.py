import cli
from setuptools import find_packages, setup

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
    package_data={"music": ["frontend/dist/**"]},
    install_requires=read("requirements.txt"),
    setup_requires=read("setup_requirements.txt"),
    entry_points={
        "console_scripts": [
            "music = music.main:main",
            "musicserver = music.backend.starter:main",
        ]
    },
)


cli.install(*read("packages.txt"))
cli.run_commands("npm install", "npm run build", cwd="music/frontend")
