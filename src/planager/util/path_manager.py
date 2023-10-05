from pathlib import Path
from typing import Optional, Union


class PathManager:  # only supports JSON for now
    declaration: Path
    derivation: Path
    tracking: Path
    txt: Path

    def __init__(self, folder: Union[Path, str]) -> None:
        self.folder = Path(folder)
        self.declaration = self.folder / "declaration.json"
        self.derivation = self.folder / "derivation.json"
        self.tracking = self.folder / "tracking.json"
        self.txt = self.folder / "txt"
