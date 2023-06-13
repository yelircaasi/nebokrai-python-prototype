from pathlib import Path

from planager import entities
from planager.utils.data.norg.norg_utils import norg_utils as norg


def read_project(filepath: Path) -> entities.Project:
    project = ...
    return project


def write_project(project: entities.Project, filepath: Path) -> None:
    ...