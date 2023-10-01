from pathlib import Path

from ..config import config
from ..planager import Planager


# def derive(root: Path) -> "Planager":
#     return Planager.from_json(root)


# def derive_from_norg(norg_workspace: Path) -> "Planager":
#     plgr = Planager.from_norg_workspace(norg_workspace)
#     return plgr


def derive_from_json(json_dir: Path) -> "Planager":
    plgr = Planager.from_json(json_dir)
    return plgr


# def derive_from_html(html_dir: Path) -> "Planager":
#     plgr = Planager.from_html(html_dir)
#     return plgr
