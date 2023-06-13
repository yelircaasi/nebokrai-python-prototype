


from pathlib import Path
from typing import Any


class Task:
    def __init__(self) -> None:
        self.x = ...


class Tasks:
    def __init__(self) -> None:
        ...

    def __getitem__(self, __name: str) -> Any:
        task = ...
        return task
    
    def __setitem__(self, __name: str, __value: Any) -> None:
        ...


class TaskPatch:
    def __init__(self) -> None:
        self.x = ...


class TaskPatches:
    def __init__(self) -> None:
        ...

    def __getitem__(self, __name: str) -> Any:
        task = ...
        return task
    
    def __setitem__(self, __name: str, __value: Any) -> None:
        ...
    
    @classmethod
    def from_norg_workspace(workspace_root: Path) -> "TaskPatches":
        patches = ...
        return patches