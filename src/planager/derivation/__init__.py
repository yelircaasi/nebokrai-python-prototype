from pathlib import Path

from planager.entities import Universe


def derive() -> "Universe":
    ...


def derive_from_norg(norg_workspace: Path) -> "Universe":
    universe = Universe.from_norg_workspace(norg_workspace)
    ...


def derive_from_json(json_dir: Path) -> "Universe":
    ...


def derive_from_html(html_dir: Path) -> "Universe":
    ...
