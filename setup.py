from setuptools import find_packages, setup

NAME = "music"


def read(filename):
    try:
        with open(filename) as fp:
            content = fp.readlines()
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
    package_data={"music": ["frontend/.**", "frontend/**"]},
    install_requires=read("requirements.txt"),
    entry_points={
        "console_scripts": [
            "music = music.main:main",
            "musicserver = music.backend.starter:main",
        ]
    },
)
