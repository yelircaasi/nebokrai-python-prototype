from pathlib import Path

from planager import entities
from planager.utils.data.norg.norg_utils import norg_utils as norg


def read_adhoc(filepath: Path) -> entities.Adhoc:
    adhoc = ...
    return adhoc


def write_adhoc(adhoc: entities.Adhoc, filepath: Path) -> None:
    ...