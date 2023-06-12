from pathlib import Path

from planager import entities


def read_roadmap(filepath: Path) -> entities.Roadmap:
    roadmap = ...
    return roadmap


def write_roadmap(roadmap: entities.Roadmap, filepath: Path) -> None:
    ...