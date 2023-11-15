from pathlib import Path

from ..planager import Planager


def derive_from_json() -> "Planager":
    plgr = Planager.from_json()
    return plgr
