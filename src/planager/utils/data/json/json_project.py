from pathlib import Path

from planager import entities


def read_project(filepath: Path) -> entities.Project:
    project = ...
    return project


def write_project(project: entities.Project, filepath: Path) -> None:
    ...