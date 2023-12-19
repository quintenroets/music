import cli
from music.backend.backend.main import Starter


def test_frontend_creation() -> None:
    def remove_frontend_dist() -> None:
        cli.run("rm -r", starter.frontend_dist, root=True)

    starter = Starter()
    existing = starter.frontend_dist.exists()
    if existing:
        remove_frontend_dist()
    starter.generate_frontend_distribution()
    if not existing:
        remove_frontend_dist()
