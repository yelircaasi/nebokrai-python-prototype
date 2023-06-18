from pathlib import Path

from planager.entities import Universe


def derive() -> "Universe":
    return Universe()


def derive_from_norg(norg_workspace: Path) -> "Universe":
    universe = Universe.from_norg_workspace(norg_workspace)
    return universe


def derive_from_json(json_dir: Path) -> "Universe":
    universe = Universe.from_json(json_dir)
    return universe


def derive_from_html(html_dir: Path) -> "Universe":
    universe = Universe.from_html(html_dir)
    return universe
