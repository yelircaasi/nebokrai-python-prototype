from pathlib import Path

from planager import entities


def read_schedule(filepath: Path) -> entities.Schedule:
    schedule = ...
    return schedule


def write_schedule(schedule: entities.Schedule, filepath: Path) -> None:
    ...