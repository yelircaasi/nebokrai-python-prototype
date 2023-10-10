from pathlib import Path

from ..planager import Planager


def derive_from_json(json_dir: Path) -> "Planager":
    plgr = Planager.from_json(json_dir)
    return plgr
