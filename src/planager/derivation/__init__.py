from pathlib import Path

from planager.entity import Planager


def derive() -> "Planager":
    return Planager()


def derive_from_norg(norg_workspace: Path) -> "Planager":
    plgr = Planager.from_norg_workspace(norg_workspace)
    return plgr


def derive_from_json(json_dir: Path) -> "Planager":
    plgr = Planager.from_json(json_dir)
    return plgr


def derive_from_html(html_dir: Path) -> "Planager":
    plgr = Planager.from_html(html_dir)
    return plgr
