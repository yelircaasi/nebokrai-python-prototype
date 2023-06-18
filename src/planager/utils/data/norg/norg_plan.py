from pathlib import Path

from planager import entities
from planager.utils.data.norg.norg_utils import norg_utils as norg


def read_plan(filepath: Path) -> entities.Plan:
    plan = ...
    return plan


def write_plan(plan: entities.Plan, filepath: Path) -> None:
    ...
