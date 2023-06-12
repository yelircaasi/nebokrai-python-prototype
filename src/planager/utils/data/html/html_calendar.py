from pathlib import Path

from planager import entities


def read_calendar(filepath: Path) -> entities.Calendar:
    calendar = ...
    return calendar


def write_calendar(calendar: entities.Calendar, filepath: Path) -> None:
    ...