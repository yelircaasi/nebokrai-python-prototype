from datetime import datetime
from pathlib import Path
from typing import Union


class PathManager:  # only supports JSON for now
    """
    Helper class to simplify working with paths in the data directory.
    """

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

    def backup(self, backup_name: str) -> Path:
        """
        Generates a path to a backup file ensuring that the backups folder exists.
        """
        backup_dir = self.folder / "backups"
        if not backup_dir.exists():
            backup_dir.mkdir()
        return backup_dir / backup_name

    def backup_with_date(self, backup_name: str) -> Path:
        """
        Generates a path to a backup file containing a timestamp.
          Ensures that the backups folder exists.
        """
        backup_dir = self.folder / "backups"
        if not backup_dir.exists():
            backup_dir.mkdir()
        split_list = backup_name.split(".")
        split_list[-2] += str(datetime.now()).split(".", maxsplit=1)[0].replace(" ", "_")
        backup_name = ".".join(split_list[:-1])
        return backup_dir / backup_name
