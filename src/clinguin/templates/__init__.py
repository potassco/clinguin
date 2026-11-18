"""Bundled Clinguin project templates."""

from importlib import resources
from pathlib import Path

TEMPLATE_FILES = ("ui.lp", "menu-bar.lp")


def create_quick_start(destination: Path, force: bool = False) -> None:
    """Copy the quick-start files into a directory."""
    targets = [destination / name for name in TEMPLATE_FILES]

    if not force:
        existing = [path.name for path in targets if path.exists()]
        if existing:
            raise FileExistsError(", ".join(existing))

    destination.mkdir(parents=True, exist_ok=True)
    source = resources.files("clinguin.templates").joinpath("quick_start")

    for name, target in zip(TEMPLATE_FILES, targets):
        target.write_bytes(source.joinpath(name).read_bytes())
