from pathlib import Path
from typing import Any, Dict, Union

from planager.utils.data.norg.norg_utils import Norg
from planager.entities import Roadmaps


class Routine:
    def __init__(
        self,
        name: str, 
        attributes: dict, 
        items: list,
    ) -> None:
        self.name = name
        self.items = items
        self.__dict__.update(attributes)
        


class Routines:
    """
    Container class for routines, designed to be 

    """
    def __init__(self) -> None:
        self.routines = {}

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
    
    @classmethod
    def from_norg_workspace(cls, workspace_dir: Path) -> "Roadmaps":
        file = workspace_dir / "routines.norg"
        parsed: Dict = Norg.from_path(file)
        routines = Routines()
        for section in parsed["sections"]:
            attributes = Norg.parse_preasterix_attributes(section)
            items = map(lambda x: x["title"], Norg.parse_subsections(section))
            
            routines.add(
                Routine(
                    section["title"], 
                    attributes, 
                    items,
                )
            )
        return routines

    