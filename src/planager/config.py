from pathlib import Path
from typing import Any


class _Config:
    def __init__(self) -> None:
        ...

    def __getitem__(self, __key: str) -> Any:
        return self.__dict__[__key]

    # def __setitem__(self, __key: str, __value: Any) -> None:
    #     self.__dict__.update({__key: __value})

    @classmethod
    def from_norg(cls, norg_path: Path) -> "ConfigType":
        return cls()  # TODO

    @classmethod
    def from_norg_workspace(cls, norg_workspace: Path) -> "ConfigType":
        norg_path = norg_workspace / "config.norg"
        return cls.from_norg(norg_path)


ConfigType = _Config
config = _Config()
