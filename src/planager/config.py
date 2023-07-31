from pathlib import Path
from typing import Any


class _Config:
    def __init__(self) -> None:
        ...

    @classmethod
    def from_norg(cls, norg_path: Path) -> "ConfigType":
        return cls()  # TODO

    @classmethod
    def from_norg_workspace(cls, norg_workspace: Path) -> "ConfigType":
        norg_path = norg_workspace / "config.norg"
        return cls.from_norg(norg_path)

    def __getitem__(self, __key: str) -> Any:
        return self.__dict__[__key]


ConfigType = _Config
config = _Config()
