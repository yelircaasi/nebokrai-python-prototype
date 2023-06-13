from pathlib import Path

from planager import entities
from planager.utils.data.norg.norg_utils import norg_utils as norg


def read_routines(filepath: Path) -> entities.Routines:
    routines = ...
    return routines


def write_routines(routines: entities.Routines, filepath: Path) -> None:
    ...