from pathlib import Path

from planager import entities


def read_plan(filepath: Path) -> entities.Plan:
    plan = ...
    return plan


def write_plan(plan: entities.Plan, filepath: Path) -> None:
    ...
