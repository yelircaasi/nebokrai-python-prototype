


from pathlib import Path
from typing import Any


class Routine:
    def __init__(self) -> None:
        self.x = ...


class Routines:
    """
    Container class for routines, designed to be 

    """
    def __init__(self) -> None:
        self.x = ...

    def __getitem__(self, __name: str) -> Routine:
        routine = ...
        return routine
    
    def __setitem__(self, __name: str, __value: Any) -> None:
        ...

    def __getattr__(self, __name: str) -> Any:
        routine = ...
        return routine
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        ...

    @classmethod
    def from_norg_workspace(cls, workspace_root: Path) -> "Routines":
        routines = cls()
        return routines