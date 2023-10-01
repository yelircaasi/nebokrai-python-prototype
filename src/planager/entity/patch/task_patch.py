from pathlib import Path
from typing import Any, Iterable, Iterator, Optional, Union

from ...util import tabularize


class TaskPatch:
    def __init__(self) -> None:
        self.x = ...


class TaskPatches:
    def __init__(self) -> None:
        ...

    @classmethod
    def from_norg_workspace(cls, workspace_dir: Path) -> "TaskPatches":
        # file = workspace_dir / "roadmaps.norg"
        # parsed = Norg.from_path(file)
        # ...
        # return cls()
        return cls()

    def __getitem__(self, __name: str) -> Any:
        task = ...
        return task

    def __setitem__(self, __name: str, __value: Any) -> None:
        ...
