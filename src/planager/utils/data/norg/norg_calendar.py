from pathlib import Path

from planager import entities
from planager.utils.data.norg.norg_utils import norg_utils as norg


def read_calendar(filepath: Path) -> entities.Calendar:
    calendar = ...
    return calendar


def write_calendar(calendar: entities.Calendar, filepath: Path) -> None:
    ...